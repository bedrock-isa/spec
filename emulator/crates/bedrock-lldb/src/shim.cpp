#include "lldb/API/SBCommandInterpreter.h"
#include "lldb/API/SBCommandReturnObject.h"
#include "lldb/API/SBDebugger.h"
#include "lldb/API/SBError.h"
#include "lldb/API/SBListener.h"
#include "lldb/API/SBProcess.h"
#include "lldb/API/SBTarget.h"

#include <cstdlib>
#include <cstring>
#include <mutex>
#include <string>

namespace {

std::once_flag g_initialize_once;

void initialize_lldb_once() {
  std::call_once(g_initialize_once, [] { lldb::SBDebugger::Initialize(); });
}

char *copy_string(const char *value) {
  if (value == nullptr) {
    value = "";
  }

  size_t len = std::strlen(value);
  char *copy = static_cast<char *>(std::malloc(len + 1));
  if (copy == nullptr) {
    return nullptr;
  }
  std::memcpy(copy, value, len);
  copy[len] = '\0';
  return copy;
}

char *copy_string(const std::string &value) { return copy_string(value.c_str()); }

void set_string(char **slot, const char *value) {
  if (slot != nullptr) {
    *slot = copy_string(value);
  }
}

void set_string(char **slot, const std::string &value) {
  if (slot != nullptr) {
    *slot = copy_string(value);
  }
}

void set_error(char **slot, const lldb::SBError &error,
               const char *fallback) {
  const char *message = error.GetCString();
  set_string(slot, message != nullptr ? message : fallback);
}

} // namespace

extern "C" {

struct bedrock_lldb_session {
  lldb::SBDebugger debugger;
  lldb::SBTarget target;
  lldb::SBProcess process;
  lldb::SBListener listener;
};

bedrock_lldb_session *bedrock_lldb_connect(const char *elf_path,
                                           const char *target_triple,
                                           const char *remote_url,
                                           char **error_out) {
  initialize_lldb_once();

  auto *session = new bedrock_lldb_session();
  session->debugger = lldb::SBDebugger::Create(false);
  if (!session->debugger.IsValid()) {
    set_string(error_out, "failed to create SBDebugger");
    delete session;
    return nullptr;
  }

  session->debugger.SetAsync(false);
  session->listener = session->debugger.GetListener();

  lldb::SBError target_error;
  const char *filename =
      (elf_path != nullptr && elf_path[0] != '\0') ? elf_path : nullptr;
  session->target = session->debugger.CreateTarget(
      filename, target_triple, nullptr, false, target_error);
  if (!session->target.IsValid() || target_error.Fail()) {
    set_error(error_out, target_error, "failed to create LLDB target");
    lldb::SBDebugger::Destroy(session->debugger);
    delete session;
    return nullptr;
  }

  // The SBTarget::ConnectRemote path leaves this gdb-remote stub in the
  // connected state; LLDB's command path performs the initial stop handshake.
  std::string connect_command = "gdb-remote ";
  constexpr const char *kConnectPrefix = "connect://";
  if (remote_url != nullptr &&
      std::strncmp(remote_url, kConnectPrefix, std::strlen(kConnectPrefix)) ==
          0) {
    connect_command += remote_url + std::strlen(kConnectPrefix);
  } else if (remote_url != nullptr) {
    connect_command += remote_url;
  }

  lldb::SBCommandReturnObject connect_result;
  session->debugger.GetCommandInterpreter().HandleCommand(
      connect_command.c_str(), connect_result);
  session->process = session->target.GetProcess();
  if (!connect_result.Succeeded() || !session->process.IsValid()) {
    std::string message = connect_result.GetError();
    if (message.empty()) {
      message = "failed to connect LLDB remote";
    }
    set_string(error_out, message);
    lldb::SBDebugger::Destroy(session->debugger);
    delete session;
    return nullptr;
  }
  session->debugger.SetAsync(true);

  return session;
}

int bedrock_lldb_command(bedrock_lldb_session *session, const char *command,
                         int *status_out, int *succeeded_out,
                         char **output_out, char **error_out) {
  if (session == nullptr || command == nullptr) {
    set_string(error_out, "invalid LLDB command session");
    return 0;
  }

  lldb::SBCommandReturnObject result;
  auto status =
      session->debugger.GetCommandInterpreter().HandleCommand(command, result);
  if (status_out != nullptr) {
    *status_out = static_cast<int>(status);
  }
  if (succeeded_out != nullptr) {
    *succeeded_out = result.Succeeded() ? 1 : 0;
  }
  set_string(output_out, result.GetOutput());
  set_string(error_out, result.GetError());
  return 1;
}

int bedrock_lldb_interrupt(bedrock_lldb_session *session, char **error_out) {
  if (session == nullptr) {
    set_string(error_out, "invalid LLDB session");
    return 0;
  }

  lldb::SBError error = session->process.Stop();
  if (error.Fail()) {
    set_error(error_out, error, "failed to stop LLDB process");
    return 0;
  }
  return 1;
}

int bedrock_lldb_detach(bedrock_lldb_session *session, char **error_out) {
  if (session == nullptr) {
    set_string(error_out, "invalid LLDB session");
    return 0;
  }

  lldb::SBError error = session->process.Detach();
  if (error.Fail()) {
    set_error(error_out, error, "failed to detach LLDB process");
    return 0;
  }
  return 1;
}

int bedrock_lldb_process_state(bedrock_lldb_session *session) {
  if (session == nullptr || !session->process.IsValid()) {
    return 0;
  }
  return static_cast<int>(session->process.GetState());
}

void bedrock_lldb_destroy(bedrock_lldb_session *session) {
  if (session == nullptr) {
    return;
  }
  if (session->process.IsValid()) {
    lldb::SBError ignored = session->process.Detach();
    (void)ignored;
  }
  lldb::SBDebugger::Destroy(session->debugger);
  delete session;
}

void bedrock_lldb_string_free(char *value) { std::free(value); }

} // extern "C"
