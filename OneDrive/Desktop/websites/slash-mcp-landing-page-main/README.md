# Slash MCP Landing Page

**Website**: [slashmcp.com](https://slashmcp.com)

A modern, interactive landing page showcasing MCP (Model Context Protocol) Servers. Discover a world where AI Agents meets MCP and explore our curated collection of MCP Servers designed to shape the future.

## 🚀 Features

- **Interactive Hero Animation**: Scroll through animated MCP server logos with smooth morphing effects
- **Modern UI**: Built with shadcn-ui components and Tailwind CSS
- **Responsive Design**: Optimized for all device sizes
- **Smooth Animations**: Powered by Framer Motion for fluid user interactions

## 🛠️ Technologies

This project is built with:

- **Vite** - Fast build tool and dev server
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **shadcn-ui** - Beautiful, accessible component library
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library

## 📦 Getting Started

### Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mcpmessenger/slash-mcp-landing-page.git
cd slash-mcp-landing-page
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:8080`

## 🏗️ Build for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

Preview the production build locally:
```bash
npm run preview
```

## 🚢 Deployment on AWS Amplify

This project is configured for deployment on AWS Amplify via GitHub.

### Automatic Deployment

1. **Connect Repository to AWS Amplify**:
   - Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
   - Click "New app" → "Host web app"
   - Select "GitHub" and authorize AWS Amplify
   - Choose the repository: `mcpmessenger/slash-mcp-landing-page`
   - Select the branch (usually `main` or `master`)

2. **Build Settings**:
   - AWS Amplify will auto-detect the build settings from `amplify.yml`
   - Build command: `npm run build`
   - Output directory: `dist`
   - Node version: 18.x or higher

3. **Deploy**:
   - Click "Save and deploy"
   - Amplify will automatically build and deploy your app
   - Future pushes to the connected branch will trigger automatic deployments

### Manual Configuration (if needed)

If auto-detection doesn't work, use these settings:

- **Build command**: `npm ci && npm run build`
- **Output directory**: `dist`
- **Node version**: 18.x

### Custom Domain

1. In AWS Amplify Console, go to your app
2. Navigate to "Domain management"
3. Click "Add domain"
4. Enter your domain (e.g., `slashmcp.com`)
5. Follow the DNS configuration instructions

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📁 Project Structure

```
slash-mcp-landing-page/
├── public/          # Static assets
├── src/
│   ├── assets/     # Images and logos
│   ├── components/ # React components
│   ├── pages/      # Page components
│   └── lib/        # Utilities
├── index.html      # HTML entry point
└── vite.config.ts  # Vite configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is private and proprietary.

## 🔗 Links

- **Website**: [slashmcp.com](https://slashmcp.com)
- **MCP Chat**: [mcp-registry-sentilabs.vercel.app/chat](https://mcp-registry-sentilabs.vercel.app/chat)
- **Repository**: [github.com/mcpmessenger/slash-mcp-landing-page](https://github.com/mcpmessenger/slash-mcp-landing-page)
