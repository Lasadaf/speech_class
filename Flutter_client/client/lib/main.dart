import 'dart:async';
import 'dart:io';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path/path.dart' as path;
import 'package:assets_audio_player/assets_audio_player.dart';
import 'package:intl/intl.dart' show DateFormat;
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:uuid/uuid.dart';

final dio = Dio();
var uuid = Uuid();

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  late FlutterSoundRecorder _recordingSession;
  final recordingPlayer = AssetsAudioPlayer();
  late String pathToAudio;
  bool _playAudio = false;
  String _timerText = '00:00:00';
  String _RecievedMessage = "";
  //var _url = Uri.http('127.0.0.1:8000');
  String _url = "http://127.0.0.1:8000";
  late String modelList;

  @override
  void initState() {
    super.initState();
    initializer();
  }
  void initializer() async {
    //pathToAudio = '/sdcard/Download/temp.wav';
    var response = await http.get(Uri.parse('http://127.0.0.1:8000/'));
    messageReceived(response.body.toString());
    pathToAudio = '/home/qwerty/Downloads/temp.wav';
    _recordingSession = FlutterSoundRecorder();
    await _recordingSession.openAudioSession(
        focus: AudioFocus.requestFocusAndStopOthers,
        category: SessionCategory.playAndRecord,
        mode: SessionMode.modeDefault,
        device: AudioDevice.speaker);
    await _recordingSession.setSubscriptionDuration(const Duration(milliseconds: 10));
    await initializeDateFormatting();
    await Permission.microphone.request();
    await Permission.storage.request();
    await Permission.manageExternalStorage.request();
    
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Center(
              child: Text(
                _timerText,
                style: const TextStyle(fontSize: 70, color: Colors.red),
              ),
            ),
            TextButton(
              onPressed: (){ startRecording(); },
              child: const Text('Start recording'),
            ),
            TextButton(
              onPressed: (){ stopRecording(); },
              child: const Text('Stop recording'),
            ),
            TextButton(
              onPressed: (){
                setState(() {
                  _playAudio = !_playAudio;
                });
                if (_playAudio) {
                  playRecording();
                } else {
                  pauseRecording();
                }
              },
              child: const Text('Play / pause recording'),
            ),
            TextButton(
              onPressed: () { sendRecording(); },
              child: const Text('Send recording'),
            ),
            Text(
              'You have received '+ _RecievedMessage,
            ),
          ],
        ),
      ),  
    ); // This trailing comma makes auto-formatting nicer for build methods.
  }
  Future<void> startRecording() async {
    Directory directory = Directory(path.dirname(pathToAudio));
    if (!directory.existsSync()) {
      directory.createSync();
    }
    _recordingSession.openAudioSession();
    await _recordingSession.startRecorder(
      toFile: pathToAudio,
      codec: Codec.pcm16WAV,
    );
    StreamSubscription recorderSubscription =
    _recordingSession.onProgress?.listen((e) {
      var date = DateTime.fromMillisecondsSinceEpoch(e.duration.inMilliseconds,
          isUtc: true);
      var timeText = DateFormat('mm:ss:SS', 'en_GB').format(date);
      setState(() {
        _timerText = timeText.substring(0, 8);
      });
    }) as StreamSubscription;
    recorderSubscription.cancel();
  }

  Future<String?> stopRecording() async {
    _recordingSession.closeAudioSession();
    return await _recordingSession.stopRecorder();
  }
  Future<void> playRecording() async {
    recordingPlayer.open(
      Audio.file(pathToAudio),
      autoStart: true,
      showNotification: true,
    );
  }
  Future<void> pauseRecording() async {
    recordingPlayer.stop();
  }

  void messageReceived(String msg){
    setState(() {
      _RecievedMessage = msg;
    });
  }

  String list_to_string(List<int> lst) {
    String out = "";
    for (int i = 0 ; i < lst.length ; i += 1) {
      out += lst[i].toString() + " ";
    }
    return out;
  }

  Future<void> sendRecording() async {
    File file = File(pathToAudio);
    var bytes = await file.readAsBytes();
    
    var data = json.encode({'uid': uuid.v4(), 'bytes': bytes});
    //print(data);
    var response = await http.post(Uri.parse('http://127.0.0.1:8000/'), headers: {'Content-Type': 'application/json'}, body: data);

    messageReceived(response.body.toString());
  }

  @override
  void dispose() {
    super.dispose();
  }

}
