using System;
using Assets.Scripts;
using UnityEngine;
using UnityEngine.EventSystems;

namespace Assets
{
    public class Ball : MonoBehaviour
    {
        private int _goalCollisions;

        private float _distanceToGoal;

        private bool _recordDistance = true;

        private bool _messageSent;

        private int _state = 0;

        private long _frameCount = 0;

        private Vector3 _startPosition;

        public float ThrowDistance = 0;

        private float _lastHeight;

        public PlayerController Thrower { get; private set; }

        public GameObject GoalPlate { get; set; }

        // Start is called before the first frame update
        void Start()
        {
            _distanceToGoal = DistanceToGoal();
            _startPosition = transform.position;
        }

        // Update is called once per frame
        void Update()
        {
            Vector3 currentPosition = transform.position;

            if (Math.Abs(currentPosition.y) <= _startPosition.y && _state >= 1)
            {
                _state = 3;

                _recordDistance = false;
            }

            if (Math.Abs(currentPosition.y) >= GoalPlate.transform.position.y && _recordDistance)
            {
                _distanceToGoal = DistanceToGoal();

                _state = 1;
            }

            if (!_recordDistance && !_messageSent || _state == 3 && !_messageSent || _frameCount > 150 && !_messageSent)
            {
                ExecuteEvents.Execute<IGoalEventTarget>(Thrower.gameObject, null, (handler, data) => handler.ResultIsIn(_distanceToGoal));
                
                _messageSent = true;

                _state = 3;

                Destroy(gameObject, 1.5f);
            }

            _frameCount++;
        }

        public void Throw(PlayerController thrower, float force, float distance)
        {
            ThrowDistance = distance;
            
            GoalPlate = GameObject.Find("SecondGoalPlate");
            
            Thrower = thrower;

            _distanceToGoal = DistanceToGoal();

            if (force <= 0 || force > 1)
            {
                _state = 1;
            }

            var from = transform.position;
            var to = GoalPlate.transform.position;
            gameObject.CreateForce(from, to, force);
        }

        private void OnTriggerEnter(Collider collision)
        {
            if (collision.gameObject.name.Contains("GoalPlate"))
            {
                HandleGoalPlateCollision(collision);
            }
        }

        private void HandleGoalPlateCollision(Collider collision)
        {
            if (_goalCollisions == 0)
            {
                if (IsGoalPlate(1, collision.gameObject))
                {
                    _goalCollisions++;
                }
            } else if (_goalCollisions == 1)
            {
                if (IsGoalPlate(2, collision.gameObject))
                {
                    _goalCollisions++;
                }
            } else if (_goalCollisions == 2)
            {
                if (IsGoalPlate(3, collision.gameObject))
                {
                    _distanceToGoal = 0;

                    _recordDistance = false;

                    _state = 4;

                    ExecuteEvents.Execute<IGoalEventTarget>(Thrower.gameObject, null, (handler, data) => handler.GoalScored(this));
                }
            }
        }

        private bool IsGoalPlate(int number, GameObject collisionObject)
        {
            var collisionName = "";

            if (number == 1)
            {
                collisionName = "First";
            } else if (number == 2)
            {
                collisionName = "Second";
            } else if (number == 3)
            {
                collisionName = "Third";
            }

            collisionName += "GoalPlate";

            return collisionObject.name.Equals(collisionName, StringComparison.OrdinalIgnoreCase);
        }

        private Vector3 VectorToGoal(bool in2D = false)
        {
            Transform target = GoalPlate.transform;

            Vector3 heading;

            if (in2D)
            {
                var gv2 = new Vector2(
                    target.position.x,
                    target.position.z);

                var tv2 = new Vector2(
                    transform.position.x, transform.position.z);

                heading = gv2 - tv2;
            }
            else
            {
                heading = target.position - transform.position;
            }

            return heading;
        }

        private float DistanceToGoal(bool in2D = false)
        {
            var pos = transform.position;

            var goal = GoalPlate.transform.position;

            var dist = (goal - pos).magnitude;

            if (pos.x > goal.x)
            {
                return dist;
            }

            if (Math.Abs(pos.x - goal.x) <= 0.3)
            {
                return 0;
            }

            return dist * -1;
        }
    }
}
