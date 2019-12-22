using System;
using System.Collections;
using System.IO;
using System.Net;
using Assets;
using Assets.Scripts;
using UnityEngine;

namespace Assets
{
    public class PlayerController : MonoBehaviour, IGoalEventTarget
    {
        private Model _model;

        public GameObject BasketBallStand;

        public GameObject Goal;

        public Ball Ball;

        private readonly object _lock = new object();

        public float? Distance { get; set; } = null;

        public float? Force { get; set; } = null;

        private float? _lastForce = null;

        public bool AskedForPrediction { get; set; } = false;

        void Start()
        {
            lock (_lock)
            {
                BasketBallStand = GameObject.Find("BasketBallStand");
                Goal = GameObject.Find("SecondGoalPlate");
                _model = new Model(this);
            }
        }

        void Update()
        {
            lock (_lock)
            {
                if (!AskedForPrediction)
                {
                    MoveToRandomPosition();
                    _model?.SendDistance();
                    SetAskedForPrediction(true);
                }
            }

            lock (_lock)
            {
                if (Distance != null)
                {
                    WriteResult((float)Distance, DistanceToGoal(), (float)_lastForce);
                }
            }

            lock (_lock)
            {
                if (Force != null)
                {
                    _lastForce = Force;
                    Shoot((float)Force);
                    ClearForce();
                }
            }
        }

        public void SetAskedForPrediction(bool didAsk)
        {
            lock (_lock)
            {
                AskedForPrediction = didAsk;
            }
        }

        public void SetDistance(float distance)
        {
            lock (_lock)
            {
                Distance = distance;
            }
        }

        public void SetForce(float force)
        {
            lock (_lock)
            {
                Force = force;
            }
        }

        public void ClearDistance()
        {
            lock (_lock)
            {
                Distance = null;
            }
        }

        public void ClearForce()
        {
            lock (_lock)
            {
                Force = null;
            }
        }

        private void WriteResult(float distance, float throwDistance, float force)
        {
            if (distance <= 0)
            {
                var file = "C:\\Users\\2803i\\OneDrive\\Skrivebord\\throws.txt";
                using (var writer = new StreamWriter(new FileStream(file, FileMode.Append, FileAccess.Write)))
                {
                    writer.WriteLine($"{distance};{throwDistance};{force}");
                }
            }
            _model?.WriteResult((float)Distance, DistanceToGoal(), (float)_lastForce);
            ClearDistance();
            SetAskedForPrediction(false);
        }

        private void Shoot(float force)
        {
            // Create the new ball
            Ball ball = Instantiate(Ball, transform.position, transform.rotation);
            // Then throw the ball
            ball.Throw(this, force, DistanceToGoal());
        }

        private void LookDirectionOfGoal()
        {
            Transform target = BasketBallStand.transform;

            Vector3 targetPosition = new Vector3(target.position.x, transform.position.y, target.position.z);

            transform.LookAt(targetPosition);
        }

        private Vector3 VectorToGoal()
        {
            Transform target = BasketBallStand.transform;

            Vector3 heading = target.position - transform.position;

            return heading;
        }

        public float DistanceToGoal()
        {
            return VectorToGoal().magnitude;
        }

        public void GoalScored(Ball ball)
        {
            Debug.Log("GOAL WAS SCORED!");
        }

        public void ResultIsIn(float distance)
        {
            SetDistance(distance);
        }

        private void MoveToRandomPosition()
        {
            // After we have shot, we move to a new random position
            gameObject.transform.position = PositionHelpers.GetRandomPosition(transform.position.y);
            // And then look towards the goal
            LookDirectionOfGoal();
        }
    }
}