using System;
using UnityEngine;

namespace Assets
{

    [Serializable]
    public struct PredictionRequest
    {
        public string Type;

        public float Distance { get; set; }

        public PredictionRequest(float distance)
        {
            Type = "request";
            Distance = distance;
        }
    }

    [Serializable]
    public struct PredictionResult
    {
        public string Type;
        public float Force;
        public float Height;

        public PredictionResult(float force, float height)
        {
            Type = "prediction";
            Force = force;
            Height = height;
        }
    }

    [Serializable]
    public struct DistanceRequest
    {
        public string Type;

        public DistanceRequest(string type = "distance")
        {
            Type = type;
        }
    }

    [Serializable]
    public struct ThrowResult
    {
        public string Type;
        public float Distance;

        public ThrowResult(float distance)
        {
            Type = "result";
            Distance = distance;
        }
    }
}