using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Assets
{
    class CourtController : MonoBehaviour
    {
        private readonly List<PlayerController> _players = new List<PlayerController>();

        public PlayerController Player;

        // Start is called before the first frame update
        void Start()
        {
            for (var i = 0; i < 4; i++)
            {
                CreatePlayer();
            }
        }

        // Update is called once per frame
        void Update()
        {
            if (Input.GetKeyUp(KeyCode.Space))
            {
                CreatePlayer();
            }

            if (Input.GetKeyUp(KeyCode.Backspace))
            {
                DeletePlayer();
            }
        }

        void CreatePlayer()
        {
            var pos = new Vector3(0, 0.925f, 0);
            Player = Instantiate(Player);
            Player.name = $"Player {_players.Count}";
            _players.Add(Player);
        }

        void DeletePlayer()
        {
            if (_players.Count <= 0)
            {
                return;
            }

            PlayerController player = _players[0];

            _players.RemoveAt(0);

            Destroy(player);
        }
    }
}