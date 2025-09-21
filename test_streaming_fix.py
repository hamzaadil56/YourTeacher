#!/usr/bin/env python3
"""
Test script to verify streaming fix
"""

import asyncio
from main import (
    screener_agent,
    StudentLearningContext,
    Runner,
    process_streaming_response
)


async def test_streaming():
    """Test the streaming functionality"""
    print("🧪 Testing Streaming Fix")
    print("=" * 30)

    try:
        # Initialize context
        context = StudentLearningContext()

        # Create input items
        input_items = [{
            "content": "Hello! I'm ready to start my personalized learning journey.",
            "role": "user"
        }]

        print("✅ Setup complete")

        # Test streaming runner
        print("🔄 Testing streaming runner...")
        streaming_result = Runner.run_streamed(
            screener_agent, input_items, context=context)
        print("✅ Streaming runner created successfully")

        # Test processing streaming response
        print("🔄 Testing streaming response processing...")
        processed_result = await process_streaming_response(streaming_result, "Test Agent")
        print("✅ Streaming response processed successfully")

        # Test accessing result properties
        print("🔄 Testing result properties...")
        input_list = processed_result.to_input_list()
        last_agent = processed_result.last_agent
        print(
            f"✅ Result properties accessed: {len(input_list)} input items, agent: {last_agent.name}")

        print("\n🎉 All streaming tests passed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def main():
    """Run streaming tests"""
    print("🎓 YourTeacher - Streaming Fix Test")
    print("=" * 40)

    success = await test_streaming()

    if success:
        print("\n✅ Streaming fix verified!")
        print("🚀 Your application is ready to run with streaming!")
        print("\nRun: python main.py")
    else:
        print("\n❌ Streaming fix needs attention")
        print("Please check the error messages above")

if __name__ == "__main__":
    asyncio.run(main())
