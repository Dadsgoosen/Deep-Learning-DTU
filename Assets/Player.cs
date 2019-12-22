/*
using System;
using System.Collections;
using UnityEngine;
using Random = System.Random;

namespace Assets
{
    public class Player : MonoBehaviour, IGoalEventTarget
    {
        public Ball Ball;

        public BasketBallStand BasketBallStand;

        public GameObject GoalPlate;

        private readonly object _lock = new object();

        private static readonly Random Random = new Random();

        // Start is called before the first frame update
        public void Start()
        {
            Model = new Model(this);
            GoalPlate = GameObject.Find("SecondGoalPlate");
            LookDirectionOfGoal();
MoveToRandomPosition();
        }

        // Update is called once per frame
        public void Update()
{
    LookDirectionOfGoal();

    if (ShootingStatus == ShootingStatus.SendingDistance)
    {

    }
}

public void OnDestroy()
{
    Model?.Dispose();
}

public void Shoot(PredictionResult prediction)
{
    Shoot(prediction.Force, prediction.Height);
}

public void Shoot(double force, double height)
{
    lock (_lock)
    {
        MoveToRandomPosition();
        LookDirectionOfGoal();
        SpawnBall();
        Ball.SetParameters(this);
        AddForce(force, height);
    }
}

private void SpawnBall()
{
    Ball = Instantiate(Ball, transform.position, transform.rotation);
}

private void MoveToRandomPosition()
{
    transform.position = GetRandomPosition();
}

private Vector3 GetRandomPosition()
{
    const int max = 5;
    float x = RandomFloat(Random, max);
    float z = RandomFloat(Random, max);
    return new Vector3(x, transform.position.y, z);
}

private static float RandomFloat(Random rand, float max)
{
    return (max * ((rand.Next() / 1073741824.0f) - 1.0f));
}

private void AddForce(double force, double height)
{

    var gv2 = new Vector2(
        GoalPlate.transform.position.x,
        GoalPlate.transform.position.z);

    var tv2 = new Vector2(
        transform.position.x, transform.position.z);

    var dir = (gv2 - tv2).normalized;

    var dist = (gv2 - tv2).magnitude;

    var arch = 0.5f;

    var closeness = Math.Min(10f, dist) / 10f;

    var forceVector = new Vector3(
        dir.x * arch * closeness,
        (float)(1f / closeness),
        dir.y * arch * closeness
    );

    // Vector3 toGoal = VectorToGoal();

    // toGoal.y += (float) height;

    // Vector3 vector =  toGoal * (float) force;

    forceVector.Scale(_scaler);

    Ball.GetComponent<Rigidbody>().AddForce(forceVector, ForceMode.Impulse);
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
    Debug.Log("GOOAALL!!");
}

public void ResultIsIn(float distance)
{
    Model.WriteResult(distance);
}
    }
}

 */

