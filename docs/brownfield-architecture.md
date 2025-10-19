# Mini Display Family Information System - Brownfield Architecture Document

## Introduction

This document captures the CURRENT STATE of the Mini Display codebase, including technical patterns, constraints, and real-world implementation details. It serves as a reference for AI agents working on the transformation from single-purpose bus display to generic family information system.

### Document Scope

**Focused on areas relevant to**: Transform existing bus arrival display into generic family information system with multiple data sources, time-based scheduling, and dynamic layouts.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2025-01-09 | 1.0 | Initial brownfield analysis for family information system transformation | John (PM Agent) |

## Quick Reference - Key Files and Entry Points

### Critical Files for Understanding the System

- **Main Entry**: `idelis-phat.py` (single-purpose application orchestrating bus display)
- **Display Models**: `display_models.py` (extensible layout and element definitions)
- **Display Devices**: `display_devices.py` (hardware abstraction for Inky/Virtual displays)
- **Display Rendering**: `display_output.py` (layout rendering and visual processing)
- **Configuration**: `config.json` (minimal configuration for bus API and display hours)
- **Font Resources**: `font_hanken_grotesk.py` (custom font handling)

### Enhancement Impact Areas (From PRD)

**Files that will be modified for family information system:**
- `idelis-phat.py` - Major refactoring to support multiple data sources
- `config.json` - Complete restructuring for hierarchical configuration
- `display_models.py` - Extensions for dynamic layout generation
- `display_output.py` - Enhancements for content type abstraction

**Files that will remain largely unchanged:**
- `display_devices.py` - Hardware abstraction is already well-designed
- Font handling system - Works correctly and can be reused

## High Level Architecture

### Technical Summary

The current system is a **single-purpose Python application** that displays bus arrival times on an e-ink display. It follows a clean modular architecture with excellent separation between display logic, hardware abstraction, and business logic. The system demonstrates solid engineering practices despite its limited scope.

### Actual Tech Stack

| Category | Technology | Version/Notes | Constraints |
|----------|------------|----------------|-------------|
| Runtime | Python 3 | 3.8+ (dataclasses usage) | Raspberry Pi environment |
| Display Library | Inky | Pimoroni Inky Phat | Hardware-specific, has fallback |
| HTTP | requests | Standard library | Single API integration |
| Image Processing | PIL/Pillow | Standard library | E-ink display rendering |
| JSON | json + nob | nob for path navigation | Configuration handling |
| Fonts | Custom | HankenGrotesk family | Embedded in Python module |
| Dependencies | Minimal | nob, requests, inky, PIL | Lightweight for Pi |

### Repository Structure Reality Check

- **Type**: Monolithic Python application (3 main modules + main script)
- **Structure**: Flat file organization, clear module boundaries
- **Notable**: Excellent display abstraction, minimal dependencies, configuration-driven
- **Deployment**: Direct Python execution, no build process

## Source Tree and Module Organization

### Project Structure (Actual)

```text
mini-display/
├── idelis-phat.py         # Main application entry point (bus-specific)
├── display_models.py      # Display layout and element definitions
├── display_devices.py     # Hardware abstraction (Inky/Virtual)
├── display_output.py      # Rendering engine and visual processing
├── config.json           # Simple configuration (API + display hours)
├── font_hanken_grotesk.py # Custom font resources
├── resources/            # Icon assets (bus-icon.png)
├── docs/                 # Project documentation
└── .bmad-core/          # Development workflow framework
```

### Key Modules and Their Purpose

- **Main Application Logic**: `idelis-phat.py` - Orchestrates data fetching, scheduling, and display rendering
- **Display Abstraction**: `display_devices.py` - Clean hardware abstraction with Inky/Virtual display support
- **Layout System**: `display_models.py` - Well-designed dataclass-based layout and element definitions
- **Rendering Engine**: `display_output.py` - Sophisticated layout rendering with horizontal/vertical arrangements
- **Configuration**: `config.json` - Minimal but functional configuration system

### Current Architecture Patterns

**Strengths:**
- Clean separation of concerns (display, hardware, business logic)
- Dataclass-based configuration with validation
- Hardware abstraction with fallback support
- Flexible layout system with validation
- Error handling and graceful degradation

**Limitations:**
- Single-purpose hardcoded business logic
- Minimal configuration system
- No abstraction for data sources
- Monolithic main application
- No support for multiple content types

## Data Models and APIs

### Display Models

**DisplayElement** (`display_models.py`):
```python
@dataclass
class DisplayElement:
    type: str  # "text" or "icon"
    alignment: str  # "top", "middle", "bottom", etc.
    size: Dict[str, Any]  # font_size or height/width
    color: str = "black"
    content: Optional[str] = None  # static content
    content_key: Optional[str] = None  # dynamic content key
    font: Optional[str] = None  # font name for text
    width_percent: Optional[float] = None  # horizontal allocation
    horizontal_align: str = "center"
    vertical_align: str = "middle"
```

**DisplayLayout** (`display_models.py`):
```python
@dataclass
class DisplayLayout:
    name: str
    elements: List[DisplayElement]
    arrangement: Optional[str] = None  # "horizontal", "vertical"
```

**Key Validation Rules:**
- Elements must have either content OR content_key (not both)
- Text elements require font and font_size
- Icon elements require content (path) and height/width
- Horizontal arrangements require width_percent on each element with the sum ≤ 100; alignment is handled per element within its block

### External API Integration

**Current API**: Idelis Transport API
- **Endpoint**: `https://api.idelis.fr/GetStopMonitoring`
- **Authentication**: X-Auth-Token header
- **Request Format**: JSON with code, ligne, next parameters
- **Response Format**: JSON with passages array
- **Error Handling**: Network exceptions, JSON parsing errors

**API Integration Pattern**:
```python
def fetch_arrival_data():
    api_token = os.getenv("IDELIS_API_TOKEN")
    response = requests.request(method='get', url=config["api_url"],
                              data=json.dumps({...}),
                              headers={'X-Auth-Token': api_token})
    return Nob(response.json())
```

## Technical Debt and Known Issues

### Critical Technical Debt

1. **Monolithic Business Logic**: All data fetching and scheduling logic is hardcoded in `idelis-phat.py`
2. **Single Data Source**: No abstraction layer for adding new data sources
3. **Minimal Configuration**: `config.json` only supports bus API parameters and display hours
4. **Hardcoded Layouts**: Display layouts are statically defined in code
5. **No Content Type System**: All content is treated as generic text/icon pairs

### Current Limitations

- **No Data Source Abstraction**: Adding new data types requires code changes
- **Static Configuration**: No support for different content types or schedules
- **Limited Layout Flexibility**: Layouts don't adapt to different content types
- **No Error Recovery**: Limited fallback options when data sources fail
- **Single Display Mode**: No support for rotating between different content types

### Workarounds and Gotchas

- **Environment Variables**: API tokens must be set as environment variables
- **Display Hardware**: Uses environment variable `INKY_DISPLAY_AVAILABLE` to switch between hardware/virtual
- **Lock File**: Uses lock file mechanism to prevent unnecessary updates during standby
- **Mock Mode**: Supports `--use-mock` flag for testing with generated data

## Integration Points and External Dependencies

### External Services

| Service | Purpose | Integration Type | Key Files |
|---------|---------|------------------|-----------|
| Idelis API | Bus arrival data | REST API (JSON) | `idelis-phat.py` |
| Environment Variables | API authentication | Runtime config | `idelis-phat.py` |
| File System | Lock files, icons | Local file I/O | `idelis-phat.py`, `display_output.py` |

### Internal Integration Points

- **Display Rendering**: Layout system → Rendering engine → Hardware abstraction
- **Configuration**: JSON config → Main application logic
- **Mock Data**: Command-line flags → Data generation → Display system
- **Error Handling**: Network failures → Fallback content → Display rendering

### Hardware Integration

- **Primary**: Inky Phat e-ink display (212x104 pixels)
- **Fallback**: Virtual display (saves to PNG file)
- **Font System**: Custom HankenGrotesk fonts embedded in Python
- **Icon Resources**: PNG files in `resources/` directory

## Development and Deployment

### Local Development Setup

**Prerequisites:**
- Python 3.8+ with dataclasses support
- Raspberry Pi environment (or simulation mode)
- Inky Phat hardware (optional - virtual display available)

**Environment Variables Required:**
```
IDELIS_API_TOKEN=your_api_token_here
INKY_DISPLAY_AVAILABLE=true/false
```

**Running the Application:**
```bash
# Normal operation with real API
python idelis-phat.py

# Mock mode for testing
python idelis-phat.py --use-mock

# Mock mode with specific time
python idelis-phat.py --use-mock --mock-time 07:30
```

### Configuration Management

**Current Configuration** (`config.json`):
```json
{
    "lock_file": "/home/user/.idelis-lock",
    "api_url": "https://api.idelis.fr/GetStopMonitoring",
    "api_code": "LAGUTS_1",
    "api_ligne": "5",
    "api_next": 3,
    "display_start_hour": 6,
    "display_start_minute": 30,
    "display_end_hour": 8,
    "display_end_minute": 30
}
```

**Configuration Constraints:**
- Single API endpoint configuration
- Fixed display hours (single time window)
- Hardcoded bus route parameters
- No support for multiple data sources

## Testing Reality

### Current Testing Approach

- **Mock Mode**: `--use-mock` flag generates simulated bus arrival data
- **Virtual Display**: `INKY_DISPLAY_AVAILABLE=false` enables file-based output
- **Manual Testing**: Primary validation method
- **No Automated Tests**: No unit tests, integration tests, or CI/CD

### Testing Capabilities

**Mock Data Generation**:
```python
def fetch_mock_arrival_data(mock_now):
    mock_passages = []
    for i in range(3):
        mock_time = (mock_now + datetime.timedelta(minutes=10 * (i + 1))).time()
        mock_passages.append({"arrivee": mock_time.strftime("%H:%M")})
    return Nob({"passages": mock_passages})
```

**Virtual Display Testing**:
- Saves rendered output as `output.png`
- Enables testing without hardware
- Supports visual validation of layouts

## Enhancement Impact Analysis

### Files That Will Need Modification

Based on the family information system transformation requirements:

#### High Impact Changes

**`idelis-phat.py` - Complete Refactoring Required**
- **Current**: Monolithic bus-specific application
- **Needed**: Generic application with data source manager
- **Changes**: Replace hardcoded logic with configurable data source system
- **Risk**: High - this is the main application entry point

**`config.json` - Complete Restructuring**
- **Current**: Simple bus API configuration
- **Needed**: Hierarchical configuration for multiple data sources
- **Changes**: Add data-source definitions, schedules, layouts sections
- **Risk**: Medium - needs migration utility for backward compatibility

#### Medium Impact Changes

**`display_models.py` - Extensions Required**
- **Current**: Static layout and element definitions
- **Needed**: Dynamic layout generation and content type system
- **Changes**: Add content type abstraction, layout templates
- **Risk**: Low-Medium - solid foundation exists

**`display_output.py` - Enhancements Required**
- **Current**: Fixed rendering for bus layouts
- **Needed**: Content-aware rendering for multiple data types
- **Changes**: Extend rendering for different content types
- **Risk**: Low - rendering system is well-designed

#### Minimal Impact Changes

**`display_devices.py` - Reuse as-is**
- **Current**: Excellent hardware abstraction
- **Needed**: No changes required
- **Changes**: None needed

### New Files/Modules Needed

#### Data Source Architecture
```
minidisplay/datasources/
├── __init__.py
├── base.py              # Abstract DataSource base class
├── manager.py           # DataSourceManager
├── idelis.py            # Refactored IdelisTransportSource
├── weather.py           # Example WeatherDataSource
└── calendar.py          # Example CalendarDataSource
```

#### Configuration System
```
config/
├── __init__.py
├── validator.py         # Configuration validation
├── migrator.py          # Configuration migration utilities
└── loader.py            # Enhanced configuration loading
```

#### Scheduling System
```
scheduling/
├── __init__.py
├── scheduler.py         # ContentScheduler
├── content_types.py     # ContentType definitions
└── templates.py         # Layout templates
```

### Integration Considerations

#### Critical Integration Points

1. **Display System Integration**
   - Must maintain compatibility with existing `DisplayLayout` and `DisplayElement`
   - Extend, don't replace, the current rendering system
   - Preserve existing validation and error handling

2. **Configuration Migration**
   - Must support existing `config.json` format
   - Provide automatic migration to new hierarchical format
   - Maintain backward compatibility during transition

3. **Data Source Abstraction**
   - Current Idelis integration must be preserved as first data source
   - New abstraction layer should be invisible to existing display logic
   - Error handling must be maintained and enhanced

#### Performance Considerations

- **Memory Usage**: Multiple data sources shouldn't exceed current usage by 50%
- **Refresh Cycles**: Total refresh time must stay under 90 seconds
- **Error Recovery**: Individual source failures shouldn't affect system performance
- **Resource Constraints**: Raspberry Pi limitations must be respected

#### Technical Constraints

- **Font System**: Must continue using existing HankenGrotesk fonts
- **Display Resolution**: Must maintain 212x104 pixel constraint
- **Hardware Abstraction**: Must preserve Inky/Virtual display flexibility
- **Environment Variables**: Must continue using environment variable authentication

## Appendix - Useful Commands and Patterns

### Frequently Used Commands

```bash
# Normal operation
python idelis-phat.py

# Testing with mock data
python idelis-phat.py --use-mock

# Testing with specific time
python idelis-phat.py --use-mock --mock-time 07:30

# Virtual display mode (no hardware)
INKY_DISPLAY_AVAILABLE=false python idelis-phat.py
```

### Development Patterns

#### Adding New Display Elements
```python
# Follow existing pattern in display_models.py
DisplayElement(
    type="text",
    content_key="new_data_key",
    alignment="middle",
    size={"font_size": 20},
    font="HankenGroteskBold",
    width_percent=50,
    horizontal_align="center",
    vertical_align="middle",
)
```

#### Extending Layout System
```python
# Current horizontal arrangement pattern
layout = DisplayLayout(
    name="New Layout",
    elements=[...],
    arrangement="horizontal"
)
```

#### Error Handling Pattern
```python
try:
    # API call or data processing
    response = requests.request(...)
    return Nob(response.json())
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    return None
```

### Debugging and Troubleshooting

- **Virtual Display Output**: Check `output.png` for rendered results
- **Error Messages**: Console output shows API errors and missing files
- **Mock Mode**: Use `--use-mock` to isolate display rendering issues
- **Configuration**: Verify JSON syntax and required fields
- **Environment**: Check environment variables for API tokens

### Common Issues and Solutions

- **Icon Not Found**: Verify icon path in `resources/` directory
- **API Authentication**: Check `IDELIS_API_TOKEN` environment variable
- **Display Not Updating**: Verify lock file permissions and display hours
- **Font Loading Errors**: HankenGrotesk fonts are embedded, check import path

---

## Enhancement Roadmap

This brownfield analysis provides the foundation for implementing the family information system transformation while preserving the excellent existing architecture and minimizing risk to current functionality.

**Key Success Factors:**
1. Maintain backward compatibility throughout the transformation
2. Leverage existing display abstraction and rendering systems
3. Implement data source abstraction as an additive layer
4. Preserve the clean separation of concerns established in the current codebase
5. Follow existing patterns for error handling and configuration management

The current system demonstrates excellent engineering practices that provide a solid foundation for the planned enhancements while maintaining the reliability and simplicity that make it effective.
