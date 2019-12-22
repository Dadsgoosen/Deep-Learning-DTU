using UnityEngine.EventSystems;

namespace Assets
{
    public interface IGoalEventTarget : IEventSystemHandler
    {
        void GoalScored(Ball ball);
        void ResultIsIn(float distance);
    }
}