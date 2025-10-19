# Mini Display Family Information System Brownfield Enhancement PRD

---

## Intro Project Analysis and Context

### Existing Project Overview

#### Analysis Source
- **IDE-based fresh analysis** - Project files analyzed directly in current environment

#### Current Project State

Based on my analysis of the existing codebase, the project is currently a **specialized bus arrival display system** with excellent architectural foundations for evolution into a generic family information display system.

**Current Implementation:**
- **Main Application**: `idelis-phat.py` - Single-purpose script focused on Idelis bus API integration
- **Display Architecture**: Well-structured modular system with `display_models.py`, `display_devices.py`, `display_output.py`
- **Current Functionality**: Displays next bus arrival time with icon + text layout
- **Hardware**: Raspberry Pi + Inky Phat e-ink display (212x104 pixels)
- **Schedule**: Active 6:30-8:30 AM, shows "En veille" outside these hours

**Architecture Strengths:**
- Clean separation of concerns (models, devices, output rendering)
- Flexible display element system supporting text and icons
- Configurable layouts with validation
- Hardware abstraction (Inky vs Virtual display)
- Mock data support for testing

### Available Documentation Analysis

#### Available Documentation
- ✅ **Project Overview** (`docs/PROJECT_OVERVIEW.md`) - Recently updated to reflect family information system vision
- ✅ **Market Research** (`docs/market-research.md`) - In progress, covers market opportunity analysis
- ❌ **Tech Stack Documentation** - Missing dedicated tech stack documentation
- ❌ **Source Tree/Architecture** - No formal architecture documentation (code analysis shows good structure)
- ❌ **Coding Standards** - No documented coding standards
- ❌ **API Documentation** - No API documentation beyond code comments
- ❌ **External API Documentation** - Limited Idelis API documentation
- ❌ **UX/UI Guidelines** - No design guidelines documented
- ❌ **Technical Debt Documentation** - No technical debt tracking

**Assessment:** Critical documentation is missing for a substantial enhancement. I recommend establishing technical documentation standards as part of this enhancement.

### Enhancement Scope Definition

#### Enhancement Type
- ✅ **New Feature Addition** (Multiple data sources)
- ✅ **Major Feature Modification** (Transform from single-purpose to generic system)
- ✅ **Integration with New Systems** (Weather APIs, Calendar APIs, etc.)
- ✅ **UI/UX Overhaul** (Dynamic layouts, multiple information types)

#### Enhancement Description
Transform the existing single-purpose bus arrival display into a **generic family information system** that can display multiple types of data (transport schedules, weather, calendar events, reminders, etc.) with configurable layouts and scheduling based on family needs and time of day.

#### Impact Assessment
- ✅ **Significant Impact** (substantial existing code changes)
  - Core application logic needs complete refactoring
  - Configuration system needs major expansion
  - Data source architecture needs complete redesign
  - Layout system needs enhancement for multiple information types

### Goals and Background Context

#### Goals
- Enable display of multiple family-relevant information types (transport, weather, calendar, reminders)
- Provide flexible configuration system for different data sources and display schedules
- Maintain existing functionality while adding extensibility
- Create architecture that supports easy addition of new data sources
- Ensure family-friendly user experience with appropriate information at different times

#### Background Context
The current system serves as an excellent proof-of-concept for e-ink display functionality but is limited to a single data source (bus schedules). The family needs a centralized display that shows relevant information throughout the day - morning commute information, afternoon weather, evening calendar events, etc. The existing architecture provides a solid foundation but needs substantial enhancement to become a truly generic family information hub.

---

## Requirements

Based on my analysis of your existing system, these requirements are designed to leverage your current architecture while enabling the generic family information system vision. Please review carefully and confirm they align with your project's reality.

### Functional

**FR1: Data Source Abstraction Layer**
The system shall support multiple data sources through a unified interface, replacing the current single-purpose Idelis API integration.

**FR2: Configuration-Driven Data Sources**
The system shall support configurable data sources via JSON configuration, allowing addition/removal of data sources without code changes.

**FR3: Multi-Information Type Support**
The system shall support display of different information types (transport, weather, calendar, reminders, etc.) with appropriate visual formatting.

**FR4: Time-Based Content Scheduling**
The system shall support different content types based on time of day and day of week, configurable per family preferences.

**FR5: Dynamic Layout Generation**
The system shall generate appropriate layouts dynamically based on content type and available display space.

**FR6: Enhanced Configuration Management**
The system shall support hierarchical configuration with global defaults, data source settings, and content-specific parameters.

**FR7: Error Handling and Graceful Degradation**
The system shall handle data source failures gracefully and display fallback content when primary sources are unavailable.

### Non Functional

**NFR1: Performance**
The system shall maintain current startup and update performance while supporting multiple data sources, with total refresh cycle not exceeding 90 seconds.

**NFR2: Memory Usage**
The system shall not exceed current memory usage by more than 50% when supporting multiple data sources and configurations.

**NFR3: Reliability**
The system shall maintain 99% uptime with individual data source failures not affecting overall system operation.

**NFR4: Maintainability**
The system architecture shall support addition of new data sources with minimal changes to core components.

**NFR5: Configuration Simplicity**
The configuration system shall remain accessible to non-technical users while supporting complex scenarios.

**NFR6: Backward Compatibility**
The system shall maintain compatibility with existing bus display functionality during transition.

### Compatibility Requirements

**CR1: Existing API Compatibility**
The current Idelis API integration shall continue to function without modification during the enhancement process.

**CR2: Display Hardware Compatibility**
The system shall maintain compatibility with existing Inky Phat display hardware specifications.

**CR3: Configuration Format Compatibility**
The existing `config.json` format shall be supported through the enhancement period with clear migration path.

**CR4: Font and Asset Compatibility**
Existing fonts and assets shall remain compatible with the enhanced layout system.

---

## Technical Constraints and Integration Requirements

### Existing Technology Stack

Based on my analysis of the current codebase, the existing technology stack is:

**Languages**: Python 3.8+ (as evidenced by dataclasses usage)
**Frameworks**:
- Custom display framework (`display_models.py`, `display_devices.py`, `display_output.py`)
- No external web frameworks detected
- PIL/Pillow for image processing
- Requests library for HTTP API calls

**Database**: No database currently used - configuration stored in JSON files
**Infrastructure**:
- Raspberry Pi environment
- E-ink display hardware (Inky Phat)
- Environment variable configuration for API tokens

**External Dependencies**:
- `nob` library for JSON path navigation
- `requests` for HTTP API calls
- `inky` library for e-ink display control
- PIL/Pillow for image processing
- Standard Python libraries (json, os, time, argparse, datetime)

### Integration Approach

**Database Integration Strategy**: No database integration required - continue using JSON configuration files with enhanced hierarchical structure for multiple data sources.

**API Integration Strategy**:
- Implement abstract data source interface to replace current Idelis-specific `fetch_arrival_data()` function
- Create concrete implementations for each data source type (weather, calendar, transport, etc.)
- Maintain existing Idelis integration as one of multiple data sources
- Add retry logic and error handling for each data source independently

**Frontend Integration Strategy**:
- Leverage existing `DisplayLayout` and `DisplayElement` architecture
- Extend layout system to support multiple content types and dynamic layout selection
- Maintain compatibility with existing font and asset system
- Add new layout templates for different information types

**Testing Integration Strategy**:
- Extend existing mock data system (`--use-mock` flag) to support multiple data source simulation
- Create individual mock generators for each data source type
- Maintain integration testing capabilities for hardware abstraction layer

### Code Organization and Standards

**File Structure Approach**:
- Maintain current modular structure
- Add new `minidisplay/datasources/` directory for data source implementations
- Add new `config/` directory for enhanced configuration management
- Keep existing `display/` components unchanged

**Naming Conventions**:
- Follow existing Python naming conventions (snake_case for functions/variables, PascalCase for classes)
- Maintain current dataclass-based model structure
- Use consistent naming for data source implementations (`*_source.py` pattern)

**Coding Standards**:
- Follow existing code style (type hints, docstrings where present)
- Maintain dataclass-based configuration approach
- Continue using environment variables for sensitive data (API tokens)
- Add comprehensive error handling following existing patterns

**Documentation Standards**:
- Add comprehensive docstrings for new data source interfaces
- Create configuration documentation for new hierarchical JSON structure
- Document integration points for adding new data sources

### Deployment and Operations

**Build Process Integration**:
- Continue using direct Python execution (no build process detected)
- Maintain current dependency management approach
- Add configuration validation on startup

**Deployment Strategy**:
- Maintain current Raspberry Pi deployment approach
- Add configuration migration utilities for existing `config.json`
- Ensure backward compatibility during transition period

**Monitoring and Logging**:
- Extend existing print-based logging with structured error reporting
- Add data source availability monitoring
- Maintain current simple operational approach

**Configuration Management**:
- Implement hierarchical JSON configuration system
- Add configuration validation and error reporting
- Maintain backward compatibility with existing configuration format
- Add configuration reload capabilities without restart

### Risk Assessment and Mitigation

**Technical Risks**:
- **Configuration Complexity**: Risk of overwhelming users with complex configuration
  - *Mitigation*: Provide sensible defaults and progressive disclosure of advanced features
- **Performance Degradation**: Multiple API calls could slow refresh cycles
  - *Mitigation*: Implement parallel data fetching and caching strategies
- **Display Layout Conflicts**: Multiple content types could create layout conflicts
  - *Mitigation*: Use existing validation system and add layout conflict detection

**Integration Risks**:
- **API Rate Limiting**: Multiple APIs could hit rate limits
  - *Mitigation*: Implement request throttling and local caching
- **Data Source Failures**: Individual source failures shouldn't break the system
  - *Mitigation*: Implement graceful degradation and fallback content
- **Hardware Resource Constraints**: Multiple data sources could strain Raspberry Pi resources
  - *Mitigation*: Monitor resource usage and implement data source prioritization

**Deployment Risks**:
- **Configuration Migration**: Existing users could face migration issues
  - *Mitigation*: Provide automated migration tools and clear documentation
- **Backward Compatibility**: Changes could break existing functionality
  - *Mitigation*: Maintain existing code paths during transition and extensive testing

**Mitigation Strategies**:
- Implement incremental rollout with feature flags
- Maintain comprehensive test coverage for existing functionality
- Create rollback procedures for each enhancement phase
- Establish monitoring for system health and performance

---

## Epic and Story Structure

Based on my analysis of your existing project, I believe this enhancement should be structured as a **single comprehensive epic** because:

1. **Architectural Cohesion**: All enhancements are interconnected through the data source abstraction layer
2. **Incremental Delivery**: Each story delivers incremental value while maintaining system integrity
3. **Risk Management**: Single epic allows coordinated rollback and testing
4. **Dependency Management**: Changes are interdependent and need coordinated implementation

The stories are designed to minimize risk to your existing system by building the abstraction layer first, then migrating existing functionality, then adding new capabilities.

**Epic Structure Decision**: Single comprehensive epic with 6 sequential stories to transform from single-purpose to generic family information system

---

## Epic 1: Family Information System Transformation

**Epic Goal**: Transform the existing bus arrival display into a generic family information system while maintaining all current functionality and adding support for multiple data sources with configurable scheduling and layouts.

**Integration Requirements**: All changes must maintain backward compatibility with existing Idelis API integration and display functionality throughout the enhancement process.

### Story 1.1 Data Source Abstraction Layer

As a system architect,
I want to create a generic data source abstraction layer,
so that the system can support multiple types of information providers (transport, weather, calendar, etc.) while maintaining the existing Idelis integration.

#### Acceptance Criteria
1. **AC1**: Create abstract `DataSource` base class with standardized interface (`fetch_data()`, `is_available()`, `get_refresh_interval()`)
2. **AC2**: Refactor existing `fetch_arrival_data()` function into `IdelisTransportSource` class implementing the new interface
3. **AC3**: Create `DataSourceManager` class to coordinate multiple data sources
4. **AC4**: Maintain exact compatibility with existing Idelis API integration and JSON response format
5. **AC5**: Add comprehensive error handling and retry logic for each data source independently
6. **AC6**: Implement data source health monitoring and availability status reporting

#### Integration Verification
**IV1**: Verify existing bus display functionality works exactly as before with no changes to visible behavior
**IV2**: Confirm data source manager properly initializes and manages the Idelis source without errors
**IV3**: Validate performance characteristics are maintained (startup time, refresh cycle duration)
**IV4**: Test error handling continues to work properly when Idelis API is unavailable

### Story 1.2 Enhanced Configuration System

As a family user,
I want to configure multiple data sources and display schedules through an enhanced JSON configuration system,
so that I can customize what information is displayed at different times of day without modifying code.

#### Acceptance Criteria
1. **AC1**: Extend `config.json` structure to support hierarchical configuration with `datasources`, `schedules`, and `layouts` sections
2. **AC2**: Create configuration validation system with clear error messages for invalid configurations
3. **AC3**: Implement backward compatibility layer that accepts existing configuration format
4. **AC4**: Add configuration migration utility to convert old format to new format
5. **AC5**: Support environment-specific configurations (development, production)
6. **AC6**: Add configuration hot-reload capability without requiring application restart

#### Integration Verification
**IV1**: Verify existing `config.json` continues to work without any modifications
**IV2**: Test configuration migration utility correctly converts existing format to new format
**IV3**: Confirm configuration validation catches invalid configurations while accepting valid ones
**IV4**: Validate system performance is not impacted by enhanced configuration parsing

### Story 1.3 Extensible Data Source Framework

As a system architect,
I want to create a framework for easily adding new data sources without modifying core system code,
so that I can add any type of family information (weather, calendar, reminders, etc.) in the future when I decide what I need.

#### Acceptance Criteria
1. **AC1**: Create base `DataSource` registration system with plugin-like architecture for easy addition of new sources
2. **AC2**: Implement data source factory pattern that can instantiate sources from configuration
3. **AC3**: Create example/template data source implementations showing patterns for common use cases
4. **AC4**: Add data source discovery and validation system
5. **AC5**: Implement flexible data transformation pipeline for different data formats
6. **AC6**: Create comprehensive documentation and examples for adding new data sources

#### Integration Verification
**IV1**: Verify the framework can load and manage multiple data source types without hardcoding
**IV2**: Test example data sources work correctly with the abstraction layer
**IV3**: Confirm new data sources can be added through configuration only
**IV4**: Validate data source isolation prevents failures in one source from affecting others

### Story 1.4 Content Type Abstraction

As a system designer,
I want to create a flexible content type system that can handle different kinds of information,
so that the display can show various data formats (text, numbers, icons, progress bars, etc.) without requiring layout changes.

#### Acceptance Criteria
1. **AC1**: Create abstract `ContentType` system that defines how different data types are displayed
2. **AC2**: Implement content type registry with built-in types (transport time, temperature, event, status, etc.)
3. **AC3**: Create content rendering pipeline that adapts to different content types
4. **AC4**: Add content type validation and formatting rules
5. **AC5**: Implement fallback content types for when specific types aren't available
6. **AC6**: Create examples showing how to add new content types

#### Integration Verification
**IV1**: Verify existing bus content type works with new content type system
**IV2**: Test content type system properly formats and displays different data formats
**IV3**: Confirm content type fallbacks work when specific types are unavailable
**IV4**: Validate new content types can be added without modifying display rendering code

### Story 1.5 Time-Based Content Scheduling

As a family user,
I want the display to show different types of information based on time of day and family schedules,
so that the most relevant information is always available when needed.

#### Acceptance Criteria
1. **AC1**: Create `ContentScheduler` class that manages which data sources are active based on time and configuration
2. **AC2**: Support multiple schedule types (time-based, day-based, priority-based)
3. **AC3**: Implement smooth transitions between different content types with appropriate timing
4. **AC4**: Add content rotation for when multiple information types should be displayed
5. **AC5**: Support family-specific schedules (weekdays vs weekends, morning vs evening)
6. **AC6**: Add manual override capabilities for temporary content changes

#### Integration Verification
**IV1**: Verify scheduling system properly switches between data sources based on configuration
**IV2**: Test existing bus display continues to work during scheduled time windows
**IV3**: Confirm content transitions are smooth and don't cause display flickering or errors
**IV4**: Validate priority-based scheduling works correctly when multiple sources are active

### Story 1.6 Dynamic Layout Generation

As a family user,
I want the display to automatically adjust layouts based on the type and amount of information being displayed,
so that all relevant information is clearly visible regardless of content type.

#### Acceptance Criteria
1. **AC1**: Extend existing `DisplayLayout` system to support dynamic layout generation based on content
2. **AC2**: Create layout templates for different content types (single item, multiple items, mixed content)
3. **AC3**: Implement content-aware layout selection that chooses appropriate template based on data
4. **AC4**: Add support for mixed-content layouts (weather + calendar, transport + weather, etc.)
5. **AC5**: Maintain backward compatibility with existing bus and standby layouts
6. **AC6**: Add layout customization options through configuration system

#### Integration Verification
**IV1**: Verify existing bus and standby layouts continue to work exactly as before
**IV2**: Test dynamic layout generation properly handles different content types and amounts
**IV3**: Confirm mixed-content layouts display multiple information types clearly and legibly
**IV4**: Validate layout selection system chooses appropriate templates based on available content

---

*PRD completed for Family Information System transformation*
