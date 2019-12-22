using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEditor;
using UnityEngine;
using Random = UnityEngine.Random;

namespace Assets
{
    public class ModelClient : IDisposable
    {
        private readonly TcpClient _client;

        private readonly StreamReader _reader;

        private readonly StreamWriter _writer;

        private readonly PlayerController _player;

        public ModelClient(string host, int port, PlayerController player)
        {
            _player = player;
            _client = new TcpClient(host, port);
            _reader = new StreamReader(_client.GetStream(), Encoding.ASCII);
            _writer = new StreamWriter(_client.GetStream(), Encoding.ASCII, 6144);
            Debug.Log($"Connected to Server {host}:{port}");
        }

        public void SendAndReceive(string message)
        {
            var t = new Thread(() =>
            {
                Task<PredictionResult> task = ReceiveMessage();

                task.Start();

                SendMessage(message);

                task.Wait();

                _player.SetForce(task.Result.Force);
            });

            t.Start();
        }

        private Task<PredictionResult> ReceiveMessage()
        {
            return new Task<PredictionResult>(() =>
            {
                object obj = null;

                const int size = 1024 * 6;

                var stream = _client.GetStream();

                while (obj == null)
                {
                    char[] buffer = new char[size];

                    StringBuilder response = new StringBuilder();

                    do
                    {
                        int read = _reader.Read(buffer, 0, buffer.Length);
                        response.Append(buffer);

                    } while (stream.DataAvailable);

                    Debug.Log($"Received {response}");

                    try
                    {
                        obj = JsonUtility.FromJson<PredictionResult>(response.ToString());
                    }
                    catch (Exception e)
                    {
                        Debug.LogException(e);
                        obj = null;
                    }
                    _reader.DiscardBufferedData();
                }
                
                return (PredictionResult) obj;
            });
        }

        public void SendMessage(string message)
        {
            Debug.Log($"Sending {message}");

            _writer.Write(message);

            _writer.Flush();
        }

        public void Dispose()
        {
            _reader?.Dispose();
            _writer?.Dispose();
            _client?.Dispose();
        }
    }
}