# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a single-file HTML Minesweeper game implementation with modern UI design. The game features two difficulty modes, a toggle-based control system (instead of left/right click), and includes timer functionality.

## Future Development Plan

### Next Project: Pygame Minesweeper
**Important**: User wants to develop the next version using Python and Pygame instead of JavaScript. This will be a native desktop application with better performance and true left/right mouse button support.

**Key improvements planned for Pygame version:**
- Native desktop application (standalone exe)
- True left/right mouse button separation
- Better graphics and animations
- Sound effects
- Local leaderboard system
- No browser dependency

## Architecture

### Single-File Structure
- **HTML**: Contains the complete game structure, CSS styling, and JavaScript logic
- **Class-based Design**: `MinesweeperGame` class encapsulates all game functionality
- **Event-driven**: Uses DOM event listeners for user interactions

### Core Components

#### Game Class (`MinesweeperGame`)
- **State Management**: Tracks game state (`ready`, `playing`, `won`, `lost`)
- **Board Generation**: Dynamic mine placement with first-click protection
- **UI Rendering**: Grid-based board with responsive cells
- **Timer System**: Countdown timer with difficulty-specific time limits

#### Key Methods
- `handleCellClick()`: Main click event handler (requires `.bind(this)` for proper scope)
- `revealCell()`: Cell revealing logic with auto-expansion for empty cells
- `revealEmptyCells()`: Recursive flood-fill for empty areas
- `renderCell()`: UI updates for cell state changes

### Critical Implementation Details

#### Event Binding Pattern
```javascript
// CORRECT: Use .bind(this) to maintain scope
cell.addEventListener('click', this.handleCellClick.bind(this));

// INCORRECT: Arrow functions lose 'this' context
cell.addEventListener('click', (e) => this.handleCellClick(e));
```

#### UI Update Pattern
When updating game state, always call both methods:
```javascript
this.revealCell(row, col);      // Update data model
this.renderCell(row, col);      // Update UI display
```

#### Recursive UI Updates
In `revealEmptyCells()`, each recursive call must update the display:
```javascript
this.revealCell(newRow, newCol);
this.renderCell(newRow, newCol);  // Critical for visual feedback
```

### Game Modes

#### Difficulty Settings
- **Easy**: 10×10 grid, 10 mines, 15 minutes (900 seconds)
- **Hard**: 16×16 grid, 40 mines, 10 minutes (600 seconds)

#### Control System
- **Toggle Switch**: Single control for mine reveal vs flag placement
- **Left-click Only**: All interactions use left-click based on toggle state

## Development Notes

### Browser Testing
- Open directly in browser: `open index.html`
- No build process or dependencies required
- Uses modern CSS features (Grid, backdrop-filter)

### Common Issues
1. **Click events not working**: Check event listener binding with `.bind(this)`
2. **Cells not updating visually**: Ensure `renderCell()` is called after state changes
3. **Recursive expansion not working**: Verify `renderCell()` is called in `revealEmptyCells()`

### CSS Styling
- Modern glassmorphism design with backdrop filters
- Responsive grid layout using CSS Grid
- Color-coded numbers for mine counts
- Black background for revealed cells with white text

## Development Requirements

### Unit Testing Policy
**Important**: All new implementations must include comprehensive unit tests after code completion.

**Testing requirements for Pygame version:**
- Test all game logic functions (mine generation, cell revealing, win/loss conditions)
- Test timer functionality and countdown behavior
- Test difficulty mode switching and configuration
- Test flag placement and removal logic
- Test recursive empty cell expansion algorithm
- Use pytest framework for Python testing
- Maintain minimum 80% code coverage

**General testing approach:**
- Write tests immediately after implementing each feature
- Test both normal operation and edge cases
- Include integration tests for user interactions
- Document any known limitations or untested scenarios

### Critical Development Practice
**Important**: Always think thoroughly before planning and implementing any feature.

**Implementation thinking process:**
- Analyze requirements completely before writing any code
- Consider all edge cases and potential failure modes
- Plan the complete architecture before starting implementation
- Think about data flow and state management
- Consider user experience and error handling
- Review existing code patterns and conventions
- Plan testing strategy alongside implementation
- Document assumptions and design decisions
- Consider performance implications and scalability
- Think about maintenance and future extensibility

**Implementation checklist:**
☐ Requirements fully understood
☐ Architecture planned and documented
☐ Edge cases identified and handled
☐ Error handling strategy defined
☐ Testing plan created
☐ Code conventions reviewed
☐ Performance considerations addressed
☐ User experience mapped out
☐ Integration points identified