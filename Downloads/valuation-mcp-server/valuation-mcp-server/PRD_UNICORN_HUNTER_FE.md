# Product Requirements Document: Unicorn Hunter Frontend

**Version:** 1.0.0  
**Date:** December 2024  
**Status:** Draft  
**Product:** Unicorn Hunter Web Application

---

## Executive Summary

**Unicorn Hunter** is a web application that allows users to analyze GitHub repositories and receive speculative valuation estimates with a gamified "unicorn score" (0-100). The application provides an intuitive interface for developers, investors, and founders to quickly assess the potential value of open-source projects.

**Core Value Proposition:** Transform complex repository metrics into an accessible, engaging valuation experience that helps users understand their project's market potential.

---

## Product Overview

### Vision Statement
Make repository valuation accessible, engaging, and actionable for everyone in the open-source ecosystem.

### Target Users

1. **Primary Users:**
   - **Developers/Founders** (40%): Want to understand their project's value
   - **Investors** (30%): Quick assessment of open-source project potential
   - **Analysts** (20%): Comparative analysis across projects
   - **Community Members** (10%): Gamified engagement with open-source

2. **User Personas:**

   **Persona 1: Sarah the Founder**
   - Early-stage startup founder
   - Wants to communicate value to investors
   - Needs quick, shareable results
   - Values simplicity and clarity

   **Persona 2: Mike the Investor**
   - VC associate evaluating open-source projects
   - Needs fast, data-driven insights
   - Values comprehensive metrics
   - Wants to compare multiple projects

   **Persona 3: Alex the Developer**
   - Open-source contributor
   - Curious about project potential
   - Values gamification and engagement
   - Wants to share results on social media

---

## Product Goals

### Primary Goals
1. **User Engagement**: 10,000+ repository analyses in first 3 months
2. **User Retention**: 30% of users return within 7 days
3. **Viral Growth**: 20% of users share results on social media
4. **Performance**: <2s average response time for analysis

### Success Metrics
- **DAU/MAU Ratio**: Target 15%+
- **Average Session Duration**: 3+ minutes
- **Bounce Rate**: <40%
- **API Success Rate**: >99%
- **User Satisfaction**: 4.5/5 stars

---

## Features & Requirements

### Phase 1: MVP (Launch)

#### 1. Repository Input & Analysis
**Priority:** P0 (Critical)

**Description:**
Users can enter a GitHub repository (owner/repo format) and receive comprehensive analysis.

**Requirements:**
- **Input Field:**
  - Text input with placeholder: "Enter GitHub repo (e.g., langchain-ai/langchain)"
  - Real-time validation for GitHub repo format
  - Auto-complete suggestions (optional, Phase 2)
  - Support for both `owner/repo` and full GitHub URLs
  
- **Analysis Trigger:**
  - "Hunt Unicorn" button (primary CTA)
  - Loading state with progress indicator
  - Error handling for invalid repos or API failures
  
- **Results Display:**
  - **Hero Section**: Large unicorn score (0-100) with status emoji
  - **Status Badge**: Color-coded tier (Seed Stage → Unicorn Alert)
  - **Valuation Ranges**: Conservative, Realistic, Optimistic (with $1B cap)
  - **Component Scores**: Breakdown of 5 factors with visual indicators
  - **Repository Metrics**: Stars, forks, contributors, activity
  - **Share Button**: Generate shareable link/image

**User Stories:**
- As a user, I want to enter a GitHub repo and see its unicorn score
- As a user, I want to understand why a repo got a specific score
- As a user, I want to share my results with others

**Acceptance Criteria:**
- ✅ User can enter `owner/repo` format
- ✅ Analysis completes in <3 seconds
- ✅ All metrics display correctly
- ✅ Error messages are clear and actionable
- ✅ Mobile-responsive design

---

#### 2. Authentication (GitHub OAuth)
**Priority:** P1 (High - for future gating)

**Description:**
GitHub OAuth integration for user authentication. Initially open (no gating), but ready for future feature gating.

**Requirements:**
- **OAuth Flow:**
  - "Sign in with GitHub" button
  - OAuth redirect to GitHub
  - Token storage (secure, httpOnly cookies)
  - User profile display (avatar, username)
  
- **Session Management:**
  - Persistent login (30-day session)
  - Logout functionality
  - Token refresh handling
  
- **Future Gating (Phase 2):**
  - Rate limiting per user
  - Premium features
  - Analysis history
  - Saved repositories

**User Stories:**
- As a user, I want to sign in with my GitHub account
- As a user, I want my session to persist across visits
- As a user, I want to see my profile information

**Acceptance Criteria:**
- ✅ OAuth flow works seamlessly
- ✅ User can sign in/out
- ✅ Session persists across browser sessions
- ✅ User profile displays correctly

---

#### 3. Results Visualization
**Priority:** P0 (Critical)

**Description:**
Engaging, visual display of analysis results with clear hierarchy and shareability.

**Requirements:**
- **Score Display:**
  - Large, animated unicorn score (0-100)
  - Circular progress indicator
  - Color gradient based on score (red → yellow → green)
  - Status text with emoji (🦄, 🚀, ⭐, 📈, 🌱, 💡)
  
- **Valuation Cards:**
  - Three cards: Conservative, Realistic, Optimistic
  - Currency formatting ($1,234,567)
  - Visual comparison (bar chart or progress bars)
  - Clear labeling of $1B cap
  
- **Component Scores:**
  - 5-factor breakdown with icons
  - Progress bars for each component
  - Tooltips explaining each factor
  - Weight indicators (25%, 20%, etc.)
  
- **Repository Stats:**
  - Grid layout with icons
  - Stars, forks, watchers, contributors
  - Activity timeline (optional, Phase 2)
  - Language badge

**User Stories:**
- As a user, I want to quickly see the unicorn score
- As a user, I want to understand the valuation ranges
- As a user, I want to see why the score is what it is

**Acceptance Criteria:**
- ✅ Score displays prominently
- ✅ All visualizations are clear and accurate
- ✅ Mobile-responsive layout
- ✅ Accessible (WCAG 2.1 AA)

---

#### 4. Error Handling & Loading States
**Priority:** P0 (Critical)

**Description:**
Graceful error handling and clear loading indicators throughout the application.

**Requirements:**
- **Loading States:**
  - Skeleton screens during analysis
  - Progress indicator with estimated time
  - Smooth transitions between states
  
- **Error Handling:**
  - Invalid repo format: "Please enter a valid GitHub repository (owner/repo)"
  - Repository not found: "Repository not found. Please check the name and try again."
  - API errors: "Unable to analyze repository. Please try again in a moment."
  - Rate limiting: "Too many requests. Please wait a moment."
  - Network errors: "Connection error. Please check your internet connection."
  
- **Empty States:**
  - Welcome message for first-time users
  - Example repositories to try
  - Clear call-to-action

**User Stories:**
- As a user, I want to know when analysis is in progress
- As a user, I want clear error messages when something goes wrong
- As a user, I want to know what to do next

**Acceptance Criteria:**
- ✅ All error states have clear messages
- ✅ Loading states provide feedback
- ✅ Users can recover from errors easily

---

### Phase 2: Enhanced Features (Post-MVP)

#### 5. Analysis History
**Priority:** P2 (Medium)

**Description:**
Save and view previously analyzed repositories (requires authentication).

**Requirements:**
- Saved analyses list
- Search/filter functionality
- Comparison view (side-by-side)
- Export to PDF/CSV

---

#### 6. Comparison Tool
**Priority:** P2 (Medium)

**Description:**
Compare multiple repositories side-by-side.

**Requirements:**
- Add multiple repos to comparison
- Side-by-side score display
- Highlight differences
- Export comparison

---

#### 7. Share & Social
**Priority:** P1 (High)

**Description:**
Enhanced sharing capabilities with visual cards.

**Requirements:**
- Generate shareable image (OG image)
- Social media preview cards
- Copy link functionality
- Embed codes for blogs

---

#### 8. Advanced Analytics
**Priority:** P3 (Low)

**Description:**
Historical tracking and trend analysis.

**Requirements:**
- Score history over time
- Trend charts
- Alerts for score changes
- Market insights

---

## Technical Architecture

### Frontend Stack

**Recommended Technology:**
- **Framework**: Next.js 14+ (React)
  - Server-side rendering for SEO
  - API routes for backend proxy
  - Image optimization
  - Built-in routing
  
- **Styling**: Tailwind CSS + shadcn/ui
  - Rapid development
  - Consistent design system
  - Responsive by default
  - Accessible components
  
- **State Management**: React Query (TanStack Query)
  - API data fetching
  - Caching and invalidation
  - Loading/error states
  
- **Authentication**: NextAuth.js
  - GitHub OAuth provider
  - Session management
  - Secure token handling
  
- **Charts/Visualization**: Recharts or Chart.js
  - Component scores visualization
  - Valuation comparison charts
  
- **Deployment**: Vercel (recommended) or Netlify
  - Zero-config deployment
  - Edge functions
  - Automatic scaling

### Backend Integration

**API Endpoint:**
```
Production: https://valuation-mcp-server-554655392699.us-central1.run.app
```

**Key Endpoints:**
1. **Health Check**: `GET /health`
2. **Manifest**: `GET /mcp/manifest`
3. **Tool Invocation**: `POST /mcp/invoke`

**Request Format:**
```json
{
  "tool": "agent_executor",
  "arguments": {
    "input": "what's the unicorn score for owner/repo?"
  }
}
```

**Response Format:**
```json
{
  "content": [{
    "type": "text",
    "text": "{ ... analysis data ... }"
  }],
  "isError": false
}
```

### Data Flow

```
User Input → Frontend Validation → API Request → MCP Server
                                                      ↓
User Interface ← Response Parsing ← API Response ← Analysis
```

### Security Considerations

1. **API Security:**
   - CORS configuration on backend
   - Rate limiting (implement in frontend)
   - Input sanitization
   - XSS prevention

2. **Authentication:**
   - Secure token storage (httpOnly cookies)
   - CSRF protection
   - Token expiration handling

3. **Data Privacy:**
   - No PII stored without consent
   - GDPR compliance considerations
   - Clear privacy policy

---

## UI/UX Design

### Design Principles

1. **Simplicity**: Clean, uncluttered interface
2. **Engagement**: Gamified elements without overwhelming
3. **Clarity**: Clear hierarchy and information architecture
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Performance**: Fast, responsive interactions

### Color Palette

**Primary Colors:**
- **Unicorn Purple**: `#8B5CF6` (vibrant, engaging)
- **Success Green**: `#10B981` (high scores)
- **Warning Yellow**: `#F59E0B` (medium scores)
- **Danger Red**: `#EF4444` (low scores)
- **Neutral Gray**: `#6B7280` (text, borders)

**Gradient:**
- Score 0-30: Red gradient
- Score 31-60: Yellow gradient
- Score 61-90: Green gradient
- Score 91-100: Purple/Unicorn gradient

### Typography

- **Headings**: Inter or Poppins (bold, modern)
- **Body**: Inter or System UI (readable, clean)
- **Scores**: Custom font or large numbers (impactful)

### Layout Structure

**Desktop:**
```
┌─────────────────────────────────────┐
│  Header (Logo, Sign In, Navigation)  │
├─────────────────────────────────────┤
│                                     │
│     Hero: Unicorn Score Display     │
│                                     │
├─────────────────────────────────────┤
│  Valuation Ranges (3 Cards)         │
├─────────────────────────────────────┤
│  Component Scores (5 Factors)       │
├─────────────────────────────────────┤
│  Repository Metrics                 │
├─────────────────────────────────────┤
│  Share Section                      │
└─────────────────────────────────────┘
```

**Mobile:**
- Stacked layout
- Full-width cards
- Collapsible sections
- Bottom navigation (optional)

### Key Components

1. **Repository Input**
   - Large, centered input field
   - Clear placeholder text
   - Prominent CTA button
   - Validation feedback

2. **Score Display**
   - Circular progress indicator
   - Large number (72pt+)
   - Status badge
   - Animated on load

3. **Valuation Cards**
   - Card-based layout
   - Icon indicators
   - Clear typography
   - Hover effects

4. **Component Scores**
   - Progress bars
   - Icon + label
   - Tooltip on hover
   - Color-coded

---

## User Flows

### Primary Flow: Repository Analysis

```
1. User lands on homepage
   ↓
2. Sees input field with example
   ↓
3. Enters "langchain-ai/langchain"
   ↓
4. Clicks "Hunt Unicorn" button
   ↓
5. Sees loading state (skeleton screen)
   ↓
6. Results appear with animation
   ↓
7. Scrolls through:
   - Unicorn score (hero)
   - Valuation ranges
   - Component scores
   - Repository metrics
   ↓
8. Clicks "Share" button
   ↓
9. Copies link or shares on social media
```

### Authentication Flow

```
1. User clicks "Sign in with GitHub"
   ↓
2. Redirected to GitHub OAuth
   ↓
3. Authorizes application
   ↓
4. Redirected back to app
   ↓
5. Session created
   ↓
6. User profile displayed in header
```

---

## API Integration Details

### Frontend API Client

**Implementation:**
```typescript
// lib/api.ts
const API_BASE_URL = 'https://valuation-mcp-server-554655392699.us-central1.run.app';

export async function analyzeRepository(repo: string) {
  const response = await fetch(`${API_BASE_URL}/mcp/invoke`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tool: 'agent_executor',
      arguments: {
        input: `what's the unicorn score for ${repo}?`
      }
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to analyze repository');
  }
  
  const data = await response.json();
  return JSON.parse(data.content[0].text);
}
```

### Error Handling

```typescript
try {
  const result = await analyzeRepository(repo);
  // Display results
} catch (error) {
  if (error.message.includes('not found')) {
    // Show "Repository not found" error
  } else if (error.message.includes('rate limit')) {
    // Show rate limit error
  } else {
    // Show generic error
  }
}
```

### Caching Strategy

- Cache successful analyses for 24 hours
- Use React Query for automatic caching
- Invalidate on manual refresh
- Store in localStorage for offline viewing

---

## Performance Requirements

### Core Web Vitals

- **LCP (Largest Contentful Paint)**: <2.5s
- **FID (First Input Delay)**: <100ms
- **CLS (Cumulative Layout Shift)**: <0.1

### API Performance

- **Analysis Response Time**: <3s (95th percentile)
- **Error Rate**: <1%
- **Uptime**: 99.9%

### Optimization Strategies

1. **Code Splitting**: Lazy load components
2. **Image Optimization**: Next.js Image component
3. **API Caching**: React Query with stale-while-revalidate
4. **CDN**: Static assets on CDN
5. **Bundle Size**: Target <200KB initial load

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance

1. **Keyboard Navigation**: All interactive elements accessible via keyboard
2. **Screen Readers**: Proper ARIA labels and semantic HTML
3. **Color Contrast**: Minimum 4.5:1 for text
4. **Focus Indicators**: Visible focus states
5. **Alt Text**: All images have descriptive alt text

### Testing

- Automated: axe-core, Lighthouse
- Manual: Screen reader testing (NVDA, JAWS)
- User testing with accessibility tools

---

## Analytics & Tracking

### Metrics to Track

1. **User Engagement:**
   - Page views
   - Unique visitors
   - Session duration
   - Bounce rate
   - Pages per session

2. **Feature Usage:**
   - Repository analyses performed
   - Share button clicks
   - Authentication sign-ups
   - Error rates

3. **Performance:**
   - API response times
   - Page load times
   - Error rates
   - Uptime

4. **Business:**
   - User acquisition sources
   - Conversion rates
   - Retention rates
   - Viral coefficient

### Tools

- **Analytics**: Google Analytics 4 or Plausible
- **Error Tracking**: Sentry
- **Performance**: Vercel Analytics or Web Vitals
- **A/B Testing**: Vercel Edge Config (future)

---

## Launch Plan

### Pre-Launch Checklist

- [ ] Frontend development complete
- [ ] API integration tested
- [ ] Authentication flow working
- [ ] Error handling implemented
- [ ] Mobile responsive
- [ ] Accessibility audit passed
- [ ] Performance optimized
- [ ] Analytics configured
- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] SEO meta tags added
- [ ] Social sharing previews configured

### Launch Strategy

**Week 1: Soft Launch**
- Limited beta testing
- Gather feedback
- Fix critical bugs
- Monitor performance

**Week 2: Public Launch**
- Announce on Product Hunt
- Share on social media
- Reach out to tech blogs
- Engage with developer communities

**Week 3-4: Iteration**
- Address user feedback
- Optimize based on analytics
- Add requested features
- Improve performance

---

## Future Roadmap

### Q1 2025
- Analysis history
- Comparison tool
- Enhanced sharing
- Mobile app (optional)

### Q2 2025
- Premium features
- API access for developers
- Webhooks for score changes
- Integration marketplace

### Q3 2025
- Historical tracking
- Trend analysis
- Market insights
- Industry benchmarks

---

## Risk Assessment

### Technical Risks

1. **API Downtime**
   - **Impact**: High
   - **Mitigation**: Error handling, fallback messages, status page

2. **Rate Limiting**
   - **Impact**: Medium
   - **Mitigation**: Implement caching, user rate limits, queue system

3. **Performance Issues**
   - **Impact**: Medium
   - **Mitigation**: Caching, CDN, optimization

### Business Risks

1. **Low User Adoption**
   - **Impact**: High
   - **Mitigation**: Marketing, viral features, partnerships

2. **GitHub API Changes**
   - **Impact**: Medium
   - **Mitigation**: Monitor API, adapt quickly

3. **Competition**
   - **Impact**: Medium
   - **Mitigation**: Unique features, superior UX, community building

---

## Success Criteria

### Launch Success (30 days)

- ✅ 1,000+ repository analyses
- ✅ 500+ registered users
- ✅ 4.0+ user rating
- ✅ <2s average response time
- ✅ <1% error rate
- ✅ 20% social sharing rate

### Long-term Success (90 days)

- ✅ 10,000+ repository analyses
- ✅ 2,000+ registered users
- ✅ 30% 7-day retention
- ✅ Featured in 3+ tech publications
- ✅ 1,000+ social media mentions

---

## Appendix

### Example API Responses

See `QUICK_START.md` and `TESTING_GUIDE.md` for detailed API examples.

### Design Mockups

(To be created by design team)

### Technical Specifications

- Browser Support: Chrome, Firefox, Safari, Edge (last 2 versions)
- Mobile Support: iOS 14+, Android 10+
- Screen Sizes: 320px - 2560px width

---

## Contact & Questions

**Product Owner:** [Name]  
**Engineering Lead:** [Name]  
**Design Lead:** [Name]  
**Backend API:** https://valuation-mcp-server-554655392699.us-central1.run.app

---

**Document Status:** Draft - Ready for Review  
**Last Updated:** December 2024  
**Next Review:** [Date]
