# Changelog

All notable changes to Android-MCP will be documented in this file.

## [1.1.0] - 2025-11-12

### Added
- **Restart-Tool**: New tool to restart device connection when experiencing timeouts or unresponsive states
  - Automatically reconnects to the device
  - Clears cached states and hanging connections
  - Returns device information after successful reconnection
  
- **max_elements parameter for State-Tool**: Control the number of UI elements returned
  - Default value: 50 elements
  - Maximum value: 200 elements
  - Minimum value: 1 element
  - Helps prevent "query result too long" errors and timeouts
  - Usage: `State-Tool(use_vision=True, max_elements=20)`

### Changed
- `State-Tool` now accepts `max_elements` parameter to limit output size
- `Mobile.get_state()` now supports `max_elements` parameter
- `Tree.get_state()` now supports `max_elements` parameter
- `Tree.get_interactive_elements()` now limits elements based on `max_elements`

### Fixed
- Fixed timeout issues when UI tree contains too many elements
- Fixed connection hanging after oversized responses
- Improved error handling in device state retrieval

### Documentation
- Added `USAGE_GUIDE.md` with detailed usage examples
- Updated `README.md` with new features
- Added `test_new_features.py` for testing new functionality

## [1.0.0] - 2025-01-XX

### Initial Release
- Basic Android device control via MCP
- UI element interaction (click, long-click, swipe, drag)
- Text input capabilities
- Screenshot and state capture
- Notification access
- Device key press support
- Wait functionality

---

## Migration Guide

### From 1.0.0 to 1.1.0

No breaking changes. All existing code will continue to work.

**Optional improvements:**

1. **Add max_elements to State-Tool calls** for better performance:
   ```python
   # Before
   State-Tool(use_vision=True)
   
   # After (recommended)
   State-Tool(use_vision=True, max_elements=50)
   ```

2. **Use Restart-Tool when experiencing timeouts**:
   ```python
   # When you get timeout errors
   Restart-Tool()
   ```

3. **Adjust max_elements based on your needs**:
   - Quick overview: `max_elements=20`
   - Normal usage: `max_elements=50` (default)
   - Detailed analysis: `max_elements=100-200`
