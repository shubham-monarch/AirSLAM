#!/usr/bin/env python3
"""
Simple script to test pyzed import and ZED SDK functionality.
"""

def test_pyzed_import():
    """Test if pyzed can be imported successfully."""
    try:
        print("Testing pyzed import...")
        import pyzed.sl as sl
        print("✅ SUCCESS: pyzed.sl imported successfully!")

        # Test basic ZED functionality
        print("\nTesting ZED SDK basic objects...")
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD720
        init_params.camera_fps = 30
        print("✅ InitParameters created successfully!")

        # Test creating camera object
        cam = sl.Camera()
        print("✅ Camera object created successfully!")

        return True

    except ImportError as e:
        print(f"❌ FAILED: Could not import pyzed.sl - {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Error during ZED SDK test - {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ZED SDK Import Test")
    print("=" * 50)

    success = test_pyzed_import()

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! ZED SDK is working correctly.")
    else:
        print("💥 Tests failed! Check ZED SDK installation.")
    print("=" * 50)
