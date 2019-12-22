using System;
using System.Globalization;

namespace Assets
{
    public class Model : IDisposable
    {
        private readonly ModelClient _client;

        private readonly PlayerController _player;

        public Model(PlayerController player)
        {
            _player = player;
            _client = new ModelClient("localhost", 5600, player);
        }

        public void SendDistance()
        {
            var distance = _player.DistanceToGoal().ToString(CultureInfo.CreateSpecificCulture("en-GB"));

            var request = "{\"type\":\"request\", \"distance\":\"" + distance + "\", \"sender\": \"" + _player.name + "\"}";

            _client.SendAndReceive(request);
        }

        public void WriteResult(float distance, float throwDistance, float force)
        {
            var distanceString = distance.ToString(CultureInfo.CreateSpecificCulture("en-GB"));
            var throwDistanceString = throwDistance.ToString(CultureInfo.CreateSpecificCulture("en-GB"));
            var forceString = force.ToString(CultureInfo.CreateSpecificCulture("en-GB"));

            var request = "{\"type\": \"result\", \"throw\": \"" + throwDistanceString + "\", \"force\": \"" + forceString + "\", " +
                          "\"distance\":\"" + distanceString + "\", \"sender\": \"" + _player.name + "\"}";

            _client.SendMessage(request);
        }

        public void Dispose()
        {
            _client?.Dispose();
        }
    }
}