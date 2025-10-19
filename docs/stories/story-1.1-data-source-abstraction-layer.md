# Story 1.1 - Data Source Abstraction Layer - Brownfield Foundation

## User Story

As a system architect,
I want to create a generic data source abstraction layer,
So that the system can support multiple types of information providers (transport, weather, calendar, etc.) while maintaining the existing Idelis integration.

## Story Context

**Existing System Integration:**

- **Integrates with**: Current Idelis API integration in `idelis-phat.py` via `fetch_arrival_data()` function
- **Technology**: Python 3.8+, requests library, JSON processing, nob library for path navigation
- **Follows pattern**: Existing error handling pattern with try/catch and None return on failure
- **Touch points**:
  - Data fetching logic in main application
  - Display rendering via `dynamic_content` dictionary
  - Configuration loading for API parameters

## Acceptance Criteria

### Functional Requirements:

1. **AC1**: Create abstract `DataSource` base class with standardized interface (`fetch_data()`, `is_available()`, `get_refresh_interval()`)
2. **AC2**: Refactor existing `fetch_arrival_data()` function into `IdelisTransportSource` class implementing the new interface
3. **AC3**: Create `DataSourceManager` class to coordinate multiple data sources (starts with just Idelis source)

### Integration Requirements:

4. **AC4**: Existing bus display functionality works exactly as before with no changes to visible behavior
5. **AC5**: New abstraction layer follows existing error handling pattern (try/catch, None return on failure)
6. **AC6**: Integration with display system maintains current `dynamic_content` dictionary structure

### Quality Requirements:

7. **AC7**: New abstraction layer includes appropriate error handling and logging
8. **AC8**: Code follows existing Python patterns and conventions used in the codebase
9. **AC9**: No regression in existing bus display functionality verified through testing

## Technical Notes

- **Integration Approach**: Create new `minidisplay/datasources/` package with base class and Idelis implementation, modify `idelis-phat.py` to use DataSourceManager instead of direct API calls
- **Existing Pattern Reference**: Follow current error handling pattern in `fetch_arrival_data()` function with try/catch and return None on failure
- **Key Constraints**: Must maintain exact compatibility with existing display rendering system, cannot change `dynamic_content` structure

## Definition of Done

- [ ] Functional requirements met (base class, IdelisTransportSource, DataSourceManager created)
- [ ] Integration requirements verified (existing bus display works unchanged)
- [ ] Existing functionality regression tested (mock mode, virtual display, real API)
- [ ] Code follows existing patterns and standards (error handling, naming conventions)
- [ ] Tests pass (existing functionality verification)
- [ ] Documentation updated if applicable (inline comments for new classes)

## Risk Assessment

- **Primary Risk**: Changes to data fetching logic could break existing bus display functionality
- **Mitigation**: Maintain exact same `dynamic_content` structure, test thoroughly with existing API integration
- **Rollback**: Simple - keep original `fetch_arrival_data()` function as backup during development

## Compatibility Verification

✅ **No breaking changes to existing APIs**: Display system interface remains unchanged
✅ **Configuration changes are additive only**: New data source configuration can be added without breaking existing `config.json`
✅ **UI changes follow existing design patterns**: No UI changes, maintains exact same visual output
✅ **Performance impact is negligible**: Minimal overhead from abstraction layer

---

*Created: 2025-01-09*
*Status: Ready for Review*
*Priority: High (Foundation for subsequent stories)*

---

## Dev Agent Record

### Agent Model Used
James (dev) - Full Stack Developer

### Debug Log References
- No debug logs created during implementation
- All components implemented following existing patterns
- Tests executed successfully with 18/18 passing

### Completion Notes List
✅ **All Functional Requirements Implemented:**
- AC1: Abstract DataSource base class with standardized interface (fetch_data, is_available, get_refresh_interval)
- AC2: IdelisTransportSource class refactored from existing fetch_arrival_data function with exact same behavior
- AC3: DataSourceManager class created to coordinate multiple data sources

✅ **All Integration Requirements Met:**
- AC4: Existing bus display functionality works exactly as before (backward compatibility maintained)
- AC5: New abstraction layer follows existing error handling pattern (try/catch, None return on failure)
- AC6: Integration with display system maintains current dynamic_content dictionary structure

✅ **All Quality Requirements Satisfied:**
- AC7: New abstraction layer includes appropriate error handling and logging
- AC8: Code follows existing Python patterns and conventions used in the codebase
- AC9: No regression in existing bus display functionality verified through comprehensive testing

### File List
**New Files Created:**
- `minidisplay/datasources/__init__.py` - Module initialization with exports
- `minidisplay/datasources/base.py` - Abstract DataSource base class
- `minidisplay/datasources/idelis.py` - IdelisTransportSource implementation
- `minidisplay/datasources/manager.py` - DataSourceManager coordination class
- `tests/datasources/test_manager.py` - Comprehensive unit tests (18 tests)

**Files Modified:**
- `idelis-phat.py` - Integrated DataSourceManager while maintaining backward compatibility

### Change Log
- **Added**: Complete data source abstraction layer
- **Refactored**: Idelis API integration into reusable component
- **Enhanced**: Error handling and logging capabilities
- **Preserved**: All existing functionality and user experience
- **Added**: Comprehensive test coverage (18 unit tests)

### Status
**Ready for Review** - All acceptance criteria met, tests passing, and integration verified
