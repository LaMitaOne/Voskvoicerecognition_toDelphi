# Voskvoicerecognition_toDelphi
Vosk Offline Voice Control for Delphi 7 and newer   
## Vosk Offline Voice Control for Delphi   
   
Simple offline voice recognition using **Vosk** (no cloud, no internet) for Delphi 7+.   
   
**Features**     
- English commands: play, next, pause, stop  
- 100% local (Vosk small English model)  
- File-based communication with Delphi (`recognized_command.txt`)  
- No Python GUI – console hidden  
- Works with any player/media app via folder monitoring  
   
**Requirements**  
- Python (`pip install sounddevice vosk`)  
- Vosk model: vosk-model-small-en-us-0.15  
  Download from: https://alphacephei.com/vosk/models  
   
**How to use**  
1. Place `vosk_offline_en.py` and model folder in your app directory  
2. Run Python script (or start via Delphi)  
3. Speak commands – recognized text goes to `SpeechCommand\recognized_command.txt`  
4. Delphi monitors folder and executes actions   
   
**Sample Delphi code** (connect to your `TFldrControl1.OnGetResult` event)    

enjoy :D   
   
```delphi   
procedure FldrControl1GetResult(Folder: String; Action: Integer);
var
  Command, XCommand: String;
  ActModifiedTime: TDateTime;
  st: TStringList;
begin
  // Change these paths to your own application paths
  const PrgPfad = 'C:\YourApp\';

  // Skip if player is busy/working (replace with your own busy check)
  if PlayerIsWorking then Exit;

  // Check for AI response file first
  if FileExists(PrgPfad + 'SpeechCommand\AIResponse.txt') then
  begin
    st := TStringList.Create;
    try
      st.LoadFromFile(PrgPfad + 'SpeechCommand\AIResponse.txt');
      if st.Count > 0 then
      begin
        XCommand := Trim(st.Strings[0]);
        // Show or log the AI response (replace with your own display method)
        ShowMessage('AI Response: ' + XCommand);
      end;
    finally
      st.Free;
    end;
    DeleteFile(PAnsiChar(PrgPfad + 'SpeechCommand\AIResponse.txt'));
  end;

  // Main voice command processing
  if FileExists(PrgPfad + 'SpeechCommand\recognized_AIcommand.txt') then
  begin
    st := TStringList.Create;
    try
      ActModifiedTime := FileAge(PrgPfad + 'SpeechCommand\recognized_AIcommand.txt');
      if LastModifiedTime <> 0 then
        if ActModifiedTime <= LastModifiedTime then Exit;
      LastModifiedTime := ActModifiedTime;

      // Retry loop if file is locked by Python
      while True do
      begin
        try
          st.LoadFromFile(PrgPfad + 'SpeechCommand\recognized_AIcommand.txt');
          Break;
        except
          on E: EFOpenError do Sleep(100);
        end;
      end;

      if st.Count = 0 then Exit;
      Command := Trim(st[0]);

      // Optional: Forward to AI if using Deepseek / external LLM
      if UseDeepseek then
      begin
        st.SaveToFile(PrgPfad + 'SpeechCommand\AIQuestion.txt');
        Exit;
      end;

      // Simple keyword matching
      XCommand := 'unrecognized';
      if Pos('play', LowerCase(Command)) > 0 then XCommand := 'play'
      else if Pos('next', LowerCase(Command)) > 0 then XCommand := 'next'
      else if Pos('stop', LowerCase(Command)) > 0 then XCommand := 'stop'
      else if Pos('pause', LowerCase(Command)) > 0 then XCommand := 'pause'
      else if Pos('random', LowerCase(Command)) > 0 then XCommand := 'random'
      else if Pos('streams', LowerCase(Command)) > 0 then XCommand := 'streams'
      else if Pos('fullscreen', LowerCase(Command)) > 0 then XCommand := 'fullscreen';

      // Optional AI fallback for unrecognized commands
      if XCommand = 'unrecognized' then
      begin
        // Replace with your own AI question method if you have one
        // Command := YourSendQuestionToAI('Interpret command: ' + Command + '. Possible commands: play next stop pause random streams fullscreen');
      end;

      // Second matching pass after possible AI interpretation
      XCommand := 'unrecognized';
      if Pos('play', LowerCase(Command)) > 0 then XCommand := 'play'
      else if Pos('next', LowerCase(Command)) > 0 then XCommand := 'next'
      else if Pos('stop', LowerCase(Command)) > 0 then XCommand := 'stop'
      else if Pos('pause', LowerCase(Command)) > 0 then XCommand := 'pause'
      else if Pos('random', LowerCase(Command)) > 0 then XCommand := 'random'
      else if Pos('streams', LowerCase(Command)) > 0 then XCommand := 'streams'
      else if Pos('fullscreen', LowerCase(Command)) > 0 then XCommand := 'fullscreen';

      if XCommand = 'unrecognized' then Exit;

      // Execute your actions here (replace with your own code)
      if XCommand = 'next' then
        // YourNextButtonClick(nil);
        ShowMessage('Next command received')
      else if XCommand = 'pause' then
        // YourPauseAction;
        ShowMessage('Pause command received')
      else if XCommand = 'play' then
        // YourPlayAction;
        ShowMessage('Play command received')
      else if XCommand = 'stop' then
        // YourStopAction;
        ShowMessage('Stop command received')
      else if XCommand = 'random' then
        // YourRandomAction;
        ShowMessage('Random command received')
      else if XCommand = 'streams' then
        // YourStreamsAction;
        ShowMessage('Streams command received')
      else if XCommand = 'fullscreen' then
        // YourFullscreenAction;
        ShowMessage('Fullscreen command received');
    finally
      st.Free;
    end;
  end
  else if FileExists(PrgPfad + 'SpeechCommand\recognized_command.txt') then
  begin
    // Standalone Vosk (no AI fallback)
    st := TStringList.Create;
    try
      ActModifiedTime := FileAge(PrgPfad + 'SpeechCommand\recognized_command.txt');
      if LastModifiedTime <> 0 then
        if ActModifiedTime <= LastModifiedTime then Exit;
      LastModifiedTime := ActModifiedTime;

      while True do
      try
        st.LoadFromFile(PrgPfad + 'SpeechCommand\recognized_command.txt');
        Break;
      except
        on E: EFOpenError do Sleep(100);
      end;

      if st.Count = 0 then Exit;
      Command := Trim(st[0]);

      // Simple command execution
      if Command = 'next' then
        // YourNextButtonClick(nil);
        ShowMessage('Next')
      else if Command = 'pause' then
        // YourPauseAction;
        ShowMessage('Pause')
      else if Command = 'play' then
        // YourPlayAction;
        ShowMessage('Play')
      else if Command = 'stop' then
        // YourStopAction;
        ShowMessage('Stop');
    finally
      st.Free;
    end;
  end;
end;

// Procedure to start the Vosk Python process
procedure StartVoskRecognition;
var
  StartupInfo: TStartupInfo;
  ProcessInfo: TProcessInformation;
  CommandLine: string;
  st: TStringList;
  i: Integer;
begin
  try
    // Change these paths to your own
    const PrgPfad = 'C:\YourApp\';
    const PythonExe = 'C:\Python312\python.exe';
    const ScriptFile = PrgPfad + 'vosk_offline_en.py';

    // Delete old command file
    DeleteFile(PChar(PrgPfad + 'SpeechCommand\recognized_command.txt'));

    // Hide console window
    ZeroMemory(@StartupInfo, SizeOf(StartupInfo));
    StartupInfo.cb := SizeOf(StartupInfo);
    StartupInfo.dwFlags := STARTF_USESHOWWINDOW;
    StartupInfo.wShowWindow := SW_HIDE;

    // Update Python script paths if needed
    if FileExists(ScriptFile) then
    begin
      st := TStringList.Create;
      try
        st.LoadFromFile(ScriptFile);
        for i := 0 to st.Count - 1 do
        begin
          if Pos('vosk-model-small-en-us', st[i]) > 0 then
            st[i] := 'model = vosk.Model(r"' + PrgPfad + 'vosk-model-small-en-us")';
          if Pos('recognized_command.txt', st[i]) > 0 then
            st[i] := 'with open(r"' + PrgPfad + 'SpeechCommand\recognized_command.txt", "w", encoding="utf-8") as file:';
        end;
        st.SaveToFile(ScriptFile);
      finally
        st.Free;
      end;
    end;

    // Start Python
    CommandLine := '"' + PythonExe + '" "' + ScriptFile + '"';

    if CreateProcess(nil, PChar(CommandLine), nil, nil, False, 0, nil, nil, StartupInfo, ProcessInfo) then
    begin
      PythonProcessHandle := ProcessInfo.hProcess;
      CloseHandle(ProcessInfo.hProcess);
      ShowMessage('Offline Voice Control started.');
    end
    else
      RaiseLastOSError;

    // Start folder monitoring (use your own folder watcher or timer)
    // Example: FldrControl1.Folder := PrgPfad + 'SpeechCommand';
    // FldrControl1.StartThread;
  except
    on E: Exception do
      ShowMessage('Error starting voice control: ' + E.Message);
  end;
end;
