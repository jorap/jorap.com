# JoRap.com - Personal Blog & Portfolio Website

<p align="center">
  <img src="assets/images/logo.png" alt="JoRap's World Logo" width="120" height="120">
</p>

<p align="center">
  <strong>A modern, fast, and SEO-optimized personal website built with Hugo and Tailwind CSS</strong>
</p>

<p align="center">
  <a href="https://jorap.com">🌐 Live Website</a> | 
  <a href="#quick-start">🚀 Quick Start</a> | 
  <a href="#for-junior-developers">👨‍💻 For Junior Devs</a> | 
  <a href="#system-architecture">🏗️ Architecture</a>
</p>

---

## 📋 Table of Contents

### 🚀 Getting Started
1. [What is this project?](#what-is-this-project)
2. [Quick Start (Get Running in 5 Minutes)](#quick-start-get-running-in-5-minutes)
3. [For Junior Developers](#for-junior-developers)
4. [Project Structure (What Files Do What)](#project-structure-what-files-do-what)
5. [How to Add Content](#how-to-add-content)
6. [Customization Guide](#customization-guide)
7. [Available Commands](#available-commands)
8. [Deployment (Going Live)](#deployment-going-live)
9. [Troubleshooting](#troubleshooting)

### 🏗️ Technical Documentation
10. [System Architecture](#system-architecture)
11. [Technical Specifications](#technical-specifications)
12. [Configuration Details](#configuration-details)
13. [Performance & SEO](#performance--seo)
14. [Security & Compliance](#security--compliance)
15. [Maintenance & Operations](#maintenance--operations)
16. [Advanced Development](#advanced-development)

### 📚 Resources
17. [Learning Resources](#learning-resources)
18. [Contributing](#contributing)
19. [License](#license)

---

## 🌟 What is this project?

JoRap.com is a **personal blog and portfolio website** that shows off:

- **Blog posts** about technology, productivity, and life experiences
- **Personal projects** and professional work
- **Resources and tutorials** for developers and tech enthusiasts

### Think of it like this:
- **Hugo** = The engine that builds your website
- **Tailwind CSS** = The styling toolkit that makes it look good
- **Markdown** = The simple way you write your blog posts
- **GitHub/Git** = Where you save and manage your code

### Why use this instead of WordPress or other platforms?

✅ **Faster** - No database, just files = super fast loading  
✅ **Cheaper** - Host for free on many platforms  
✅ **Safer** - No server to hack, just static files  
✅ **Developer-friendly** - Everything is code, easy to customize  
✅ **SEO-friendly** - Google loves fast, clean sites  

### System Overview
- **Project Name**: JoRap's World
- **Website URL**: https://jorap.com
- **System Type**: Static Site Generator (Hugo-based)
- **Current Version**: 2.1.2
- **License**: MIT
- **Author**: JoRap

---

## 🚀 Quick Start (Get Running in 5 Minutes)

### Step 1: Install Required Tools

You need these tools installed on your computer:

1. **Hugo Extended** v0.141.0+ 
   - Download: https://gohugo.io/installation/
   - ⚠️ **IMPORTANT**: Get the "extended" version (not regular)

2. **Node.js** v16+
   - Download: https://nodejs.org/
   - Choose the "LTS" version

3. **Go** v1.21+
   - Download: https://golang.org/dl/
   - Hugo needs this for modules

4. **Git** 
   - Download: https://git-scm.com/

### Step 2: Download and Setup

```bash
# 1. Download the project
git clone https://github.com/yourusername/jorap.com.git
cd jorap.com

# 2. Install dependencies
npm install

# 3. Set up the project structure
npm run project-setup

# 4. Start the development server
npm run dev
```

### Step 3: Open Your Browser

Go to `http://localhost:1313` - you should see the website running! 🎉

---

## 👨‍💻 For Junior Developers

### What you'll learn working on this project:

- **Static Site Generation** - How modern websites are built
- **Markdown** - Simple way to write content
- **Git workflows** - Professional version control
- **CSS frameworks** - Using Tailwind CSS
- **Deployment** - Getting your site live
- **Performance optimization** - Making sites fast
- **SEO basics** - Getting found on Google

### Key concepts to understand:

#### Static Site Generation
- **Traditional websites**: Server generates pages when users visit
- **Static websites**: All pages are pre-built as HTML files
- **Result**: Much faster loading, cheaper hosting, more secure

#### How Hugo Works
```
Your Markdown + Templates + Configuration → Hugo → Static HTML Website
```

#### Development vs Production
- **Development**: `npm run dev` - rebuilds on every change
- **Production**: `npm run build` - optimized for deployment

---

## 📁 Project Structure (What Files Do What)

```
jorap.com/
├── 📁 assets/           # Static assets (CSS, JS, images)
│   ├── css/            # Custom stylesheets
│   ├── images/         # Your images (photos, logos, etc.)
│   └── js/             # JavaScript files
├── 📁 config/          # Hugo configuration files
│   └── _default/       # Main configuration files
│       ├── hugo.toml       # Main configuration
│       ├── params.toml     # Site parameters
│       ├── menus.en.toml   # Navigation menus
│       ├── languages.toml  # Language settings
│       └── module.toml     # Hugo modules
├── 📁 content/         # Markdown content files
│   └── english/        # English content
│       ├── _index.md       # Homepage content
│       ├── blog/           # Blog posts go here
│       ├── authors/        # Author profiles
│       ├── contact/        # Contact information
│       ├── pages/          # Static pages
│       └── sections/       # Reusable content sections
├── 📁 data/            # Data files (JSON/YAML)
│   ├── settings.json   # Site settings
│   ├── social.json     # Social media links
│   └── theme.json      # Colors and fonts
├── 📁 themes/          # Website design and layout
│   └── jorap/          # Custom theme
│       ├── assets/         # Theme assets
│       ├── layouts/        # HTML templates
│       └── static/         # Static theme files
├── 📁 scripts/         # Build and maintenance scripts
├── 📁 static/          # Static files served as-is
├── 📁 public/          # Generated static site (build output)
├── 📄 hugo.toml        # Main settings file
├── 📄 package.json     # Lists all tools and commands
└── 📄 README.md        # This file!
```

### Files beginners should know:

| File                          | What it does                             |
| ----------------------------- | ---------------------------------------- |
| `hugo.toml`                   | Main website settings (title, URL, etc.) |
| `config/_default/params.toml` | Website appearance settings              |
| `content/english/blog/`       | Where your blog posts live               |
| `data/theme.json`             | Colors and fonts                         |
| `data/social.json`            | Social media links                       |
| `package.json`                | Available commands and tools             |

---

## 📝 How to Add Content

### Creating a New Blog Post

1. **Create a new file** in `content/english/blog/`
2. **Name it** like `my-awesome-post.md`
3. **Add frontmatter** (metadata) at the top:

```markdown
---
title: "My Awesome Post"
description: "A short description for SEO"
date: 2024-01-01T10:00:00Z
author: "Your Name"
categories: ["Technology"]
tags: ["Hugo", "Web Development"]
image: "images/my-post-image.jpg"
draft: false
---

# Your Post Content Goes Here

Write your blog post using **Markdown** syntax.

## You can add subheadings

- Bullet points
- Are easy

1. Numbered lists
2. Work too

```code blocks are supported```

![Images work too](images/my-image.jpg)
```

### Understanding Frontmatter

Frontmatter is the metadata at the top of your file:

```yaml
---
title: "Post Title"           # Required: Shows in browser tab
description: "SEO description" # Appears in Google search results
date: 2024-01-01T10:00:00Z    # When you published it
author: "Your Name"           # Must match author in authors/ folder
categories: ["Tech"]          # Main topic (appears in URL)
tags: ["Hugo", "CSS"]         # Specific topics (for filtering)
image: "images/post.jpg"      # Featured image
draft: false                  # true = hidden, false = published
---
```

### Adding Images

1. **Add image files** to `assets/images/`
2. **Reference them** in your content:
   ```markdown
   ![Description of image](images/my-image.jpg)
   ```

### Creating Author Profiles

1. **Create file** in `content/english/authors/your-name.md`
2. **Add information**:

```markdown
---
title: "Your Name"
email: "your.email@example.com"
image: "images/your-photo.jpg"
description: "Brief bio about yourself"
social:
  - name: "twitter"
    icon: "fab fa-twitter"
    link: "https://twitter.com/yourusername"
  - name: "github"
    icon: "fab fa-github"
    link: "https://github.com/yourusername"
---

Extended bio content here...
```

---

## 🎨 Customization Guide

### Basic Site Settings

Edit `hugo.toml`:

```toml
# Basic Information
baseURL = "https://yoursite.com"
title = "Your Site Title"
languageCode = "en"
defaultContentLanguage = "en"

# Theme
theme = "jorap"
```

### Site Appearance

Edit `config/_default/params.toml`:

```toml
# Branding
logo = "images/logo.png"
logo_darkmode = "images/logo-dark.png"
favicon = "images/favicon.png"

# Features
search = true              # Enable search
cookie_consent = true      # Show cookie banner
theme_switcher = true      # Enable dark/light mode toggle
```

### Colors and Fonts

Edit `data/theme.json`:

```json
{
  "colors": {
    "primary": "#3B82F6",      // Main accent color
    "secondary": "#1E40AF",    // Secondary accent
    "dark": "#1F2937",         // Dark mode background
    "light": "#F9FAFB"         // Light mode background
  },
  "fonts": {
    "primary": "Inter, sans-serif",
    "secondary": "Roboto, sans-serif"
  }
}
```

### Social Media Links

Edit `data/social.json`:

```json
[
  {
    "name": "GitHub",
    "icon": "fab fa-github",
    "link": "https://github.com/yourusername"
  },
  {
    "name": "Twitter",
    "icon": "fab fa-twitter",
    "link": "https://twitter.com/yourusername"
  },
  {
    "name": "LinkedIn",
    "icon": "fab fa-linkedin",
    "link": "https://linkedin.com/in/yourusername"
  }
]
```

---

## 🛠️ Available Commands

### Daily Development Commands

```bash
# Start development server (most common)
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Format code with Prettier
npm run format
```

### Setup Commands

```bash
# Initial project setup (run once)
npm run project-setup

# Update Hugo modules
npm run update-modules

# Update theme to latest version
npm run update-theme
```

### Utility Commands

```bash
# Set up theme structure
npm run theme-setup

# Remove dark mode feature
npm run remove-darkmode

# Clear modules cache
npm run clear-modules
```

---

## 🚀 Deployment (Going Live)

### Multi-Platform Deployment Support

This project supports deployment on multiple platforms with optimized configurations:

#### Option 1: AWS Amplify (Recommended)

**Configuration**: `amplify.yml`
- **Hugo Version**: 0.141.0
- **Go Version**: 1.23.3
- **Build Command**: `npm run project-setup && npm run build`
- **Output Directory**: `/public`

1. **Push to GitHub**
2. **Connect** to AWS Amplify
3. **Auto-deployment** with the included configuration

#### Option 2: Netlify (Easiest for Beginners)

**Configuration**: `netlify.toml`
- **Hugo Version**: 0.146.5
- **Go Version**: 1.24.2
- **Build Command**: `yarn project-setup; yarn build`
- **Publish Directory**: `public`

1. **Build your site**:
   ```bash
   npm run build
   ```

2. **Go to [netlify.com](https://netlify.com)**

3. **Drag the `public` folder** to the deploy area

4. **Your site is live!** 🎉

#### Option 3: Vercel (Git-based)

**Configuration**: `vercel.json`
- **Build Script**: `vercel-build.sh`
- **Static Build**: `@vercel/static-build`
- **Output Directory**: `public`

1. **Push your code** to GitHub
2. **Connect** your GitHub repo to [vercel.com](https://vercel.com)
3. **Auto-deployment** happens on every push

### Before You Deploy

1. **Update your site URL** in `hugo.toml`:
   ```toml
   baseURL = "https://yoursite.com"
   ```

2. **Test locally**:
   ```bash
   npm run build
   npm run preview
   ```

3. **Check everything works** at `http://localhost:1313`

---

## 🔧 Troubleshooting

### Common Problems and Solutions

#### "Hugo not found" or "Hugo command not found"

**Problem**: Hugo isn't installed or not in your PATH  
**Solution**: 
1. Install Hugo Extended from https://gohugo.io/installation/
2. Make sure it's the "extended" version
3. Restart your terminal/command prompt

#### "Module not found" errors

**Problem**: Hugo modules aren't set up correctly  
**Solution**:
```bash
npm run update-modules
```

#### Styles not loading or site looks broken

**Problem**: CSS isn't building correctly  
**Solution**:
```bash
rm -rf node_modules
npm install
npm run dev
```

#### Images not showing

**Problem**: Wrong image paths  
**Solution**:
- Make sure images are in `assets/images/`
- Use relative paths: `images/my-image.jpg`
- Check file names match exactly (case-sensitive)

#### Build fails with errors

**Problem**: Various build issues  
**Solution**:
```bash
# Nuclear option - start fresh
rm -rf node_modules
rm -rf resources
rm -rf public
npm install
npm run project-setup
npm run build
```

### Getting Help

1. **Read the error message** - it usually tells you what's wrong
2. **Check [Hugo documentation](https://gohugo.io/documentation/)**
3. **Ask on [Hugo forums](https://discourse.gohugo.io/)**
4. **Search Google** for the specific error

---

# 🏗️ Technical Documentation

> **Note**: The sections below are for advanced users, system administrators, and developers who need detailed technical information about the system architecture and specifications.

---

## System Architecture

### Core Technology Stack

| Technology       | Version   | Purpose                    |
| ---------------- | --------- | -------------------------- |
| **Hugo**         | v0.141.0+ | Static site generator      |
| **Tailwind CSS** | v4.1.4    | CSS framework              |
| **Go**           | v1.21+    | Required by Hugo modules   |
| **Node.js**      | v16+      | Build tools and processing |

### System Dependencies

#### Hugo Modules
- `github.com/gethugothemes/hugo-modules/accordion`
- `github.com/gethugothemes/hugo-modules/components/announcement`
- `github.com/gethugothemes/hugo-modules/components/cookie-consent`
- `github.com/gethugothemes/hugo-modules/components/preloader`
- `github.com/gethugothemes/hugo-modules/components/social-share`
- `github.com/gethugothemes/hugo-modules/gallery-slider`
- `github.com/gethugothemes/hugo-modules/search`
- `github.com/gethugothemes/hugo-modules/seo-tools/basic-seo`
- `github.com/hugomods/mermaid` (v0.1.4)

#### Development Dependencies
```json
{
  "@tailwindcss/cli": "^4.1.4",
  "@tailwindcss/forms": "^0.5.10",
  "@tailwindcss/typography": "^0.5.16",
  "prettier": "^3.5.3",
  "prettier-plugin-go-template": "0.0.15",
  "prettier-plugin-tailwindcss": "^0.6.11",
  "tailwindcss": "^4.1.4"
}
```

### Frontend Components
- **Theme System**: Custom "jorap" theme based on Hugoplate
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark Mode**: System/user preference with theme switcher
- **Search Functionality**: Built-in search with indexed content
- **Image Processing**: Hugo's built-in image processing with WebP support

### Content Management
- **Content Types**: Blog posts, pages, authors
- **Taxonomies**: Categories and tags
- **Multi-language Support**: English (default), extensible
- **Content Structure**: Organized by content type and language

---

## Technical Specifications

### Hugo Configuration (`hugo.toml`)
- **Base URL**: Configurable (default: "/")
- **Title**: "JoRap's World"
- **Theme**: "jorap"
- **Timezone**: Asia/Manila
- **Default Language**: English
- **Summary Length**: 10 words
- **Permalink Structure**: Custom for pages
- **Pagination**: 10 items per page

### Build System

#### Build Process
```bash
# Development
npm run dev                 # Start development server
npm run preview            # Preview production build
npm run watch              # Watch mode with minification

# Production
npm run build              # Full production build
npm run update-modules     # Update Hugo modules
```

#### Build Pipeline
1. **Pre-build**: Clear modules, update dependencies
2. **Asset Processing**: Compile CSS, optimize images
3. **Content Processing**: Render Markdown to HTML
4. **Optimization**: Minify HTML/CSS/JS, generate manifests
5. **Output**: Static files in `/public` directory

#### Build Optimization
- **Template Metrics**: Performance monitoring enabled
- **Asset Minification**: CSS/JS minification in production
- **Image Processing**: WebP conversion, responsive images
- **Caching**: Built-in caching for assets and images (720h)
- **Build Statistics**: Enabled for performance analysis

---

## Configuration Details

### Site Parameters (`params.toml`)
- **Logo**: Custom JoRap logo (60px x 60px)
- **Theme Switcher**: Enabled (light/dark/system)
- **Search**: Enabled with full-text search
- **SEO**: Comprehensive meta tags and OpenGraph
- **Analytics**: Google Analytics ready
- **Social Sharing**: Enabled
- **Cookie Consent**: Configurable

### Content Features
- **Blog System**: Full-featured blogging with categories/tags
- **Author Profiles**: Multi-author support
- **Image Optimization**: Automatic WebP conversion
- **Table of Contents**: Auto-generated for long content
- **Syntax Highlighting**: Monokai theme
- **Social Sharing**: Built-in sharing buttons
- **RSS Feeds**: Auto-generated feeds

### User Interface Specifications

#### Design System
- **CSS Framework**: Tailwind CSS 4.1.4
- **Typography**: System fonts with fallbacks
- **Color Scheme**: Adaptive (light/dark mode)
- **Responsive Breakpoints**: Mobile-first design
- **Icons**: Font Awesome 6 (brands, solid, icons)

#### Navigation Structure
```
Main Navigation:
├── Home (/)
├── About (/about)
├── Blog (/blog)
├── Categories (/categories)
└── Tags (/tags)

Footer Navigation:
├── About (/about)
├── Categories (/categories)
└── Tags (/tags)
```

#### Page Types
- **Homepage**: Banner, features, call-to-action
- **Blog List**: Paginated blog post listings
- **Blog Single**: Individual blog post with sharing
- **About**: Personal information and bio
- **Categories/Tags**: Taxonomy listings
- **Contact**: Contact form and information
- **404**: Custom error page

---

## Performance & SEO

### Performance Targets
- **Google PageSpeed Score**: 95+
- **Core Web Vitals**: Optimized for all metrics
- **Time to First Byte**: <200ms
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s

### Optimization Features
- **Static Generation**: Pre-built HTML pages
- **Image Optimization**: WebP conversion, lazy loading
- **Asset Minification**: CSS/JS minification
- **Caching**: Browser and CDN caching
- **Tree Shaking**: Unused CSS/JS removal

### SEO Features
- **Meta Tags**: Comprehensive meta tag support
- **OpenGraph**: Social media sharing optimization
- **Twitter Cards**: Twitter-specific metadata
- **Structured Data**: JSON-LD support
- **Sitemap**: Auto-generated XML sitemap
- **Robots.txt**: Search engine directives

### Analytics Integration
- **Google Analytics**: GA4 support (configurable)
- **Google Tag Manager**: GTM integration ready
- **Search Console**: Site verification support
- **Custom Tracking**: Event tracking capabilities

### CDN and Performance
- **Static Assets**: Served via CDN
- **Image Optimization**: Automatic format conversion
- **Caching Strategy**: Long-term caching for assets
- **Compression**: Gzip enabled

---

## Security & Compliance

### Content Security
- **Markdown Rendering**: Safe HTML rendering with goldmark
- **User Input**: Contact forms via external services
- **XSS Protection**: Built-in Hugo protections
- **HTTPS**: Enforced on all platforms

### Privacy and Compliance
- **Cookie Consent**: Configurable cookie banner
- **Analytics**: Privacy-focused implementation
- **Data Collection**: Minimal user data collection
- **GDPR**: Cookie consent and privacy policy ready

---

## Maintenance & Operations

### Regular Maintenance Tasks
- **Dependency Updates**: Monthly Hugo and npm package updates
- **Content Backup**: Regular content repository backups
- **Performance Monitoring**: Monthly performance audits
- **Security Updates**: Apply security patches promptly
- **Link Checking**: Quarterly broken link audits

### Monitoring and Logging
- **Build Monitoring**: Deployment status tracking
- **Performance Monitoring**: Core Web Vitals tracking
- **Error Monitoring**: 404 and error page tracking
- **Analytics Review**: Monthly traffic and engagement review

### Backup and Recovery
- **Source Code**: Git repository with remote backups
- **Content**: Version-controlled Markdown files
- **Configuration**: All settings in version control
- **Recovery Time**: <30 minutes for full site restore

### Content Management Workflow
1. **Write**: Create Markdown files with YAML frontmatter
2. **Organize**: Place in appropriate content directories
3. **Preview**: Use development server for preview
4. **Publish**: Commit to Git, automatic deployment

---

## Advanced Development

### Local Development Setup
```bash
# Clone repository
git clone [repository-url]
cd jorap.com

# Install dependencies
npm install

# Run project setup
npm run project-setup

# Start development server
npm run dev
```

### Code Quality
- **Prettier**: Code formatting for consistent style
- **Hugo Linting**: Template and configuration validation
- **Accessibility**: WCAG 2.1 compliance target
- **Performance**: Regular Core Web Vitals auditing

### Extensibility and Customization

#### Theme Customization
- **CSS Customization**: Tailwind CSS configuration
- **Layout Overrides**: Template customization in themes/
- **Component Addition**: Custom Hugo shortcodes
- **JavaScript Enhancement**: Custom JS in assets/

#### Content Extension
- **New Content Types**: Add new archetypes
- **Custom Fields**: Extend frontmatter schemas
- **Taxonomies**: Add new classification systems
- **Multilingual**: Add new language support

#### Feature Addition
- **Hugo Modules**: Extend with additional modules
- **Third-party Services**: API integrations
- **Custom Shortcodes**: Reusable content components
- **Plugin System**: Via Hugo modules ecosystem

### System Requirements

#### Development Environment
- **Operating System**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Node.js**: 16+ LTS
- **Go**: 1.21+
- **Hugo**: 0.141.0+ (extended version)
- **Git**: 2.20+

#### Production Environment
- **Hosting**: Static hosting (Netlify, Vercel, AWS Amplify)
- **CDN**: Automatic via hosting platform
- **SSL**: Automatic certificate management
- **Domain**: Custom domain support

#### Browser Support
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Android 90+
- **Graceful Degradation**: Basic functionality on older browsers

### Debugging Tools
- **Hugo Server**: Development server with live reload
- **Template Metrics**: Performance debugging
- **Build Statistics**: Asset analysis
- **Browser DevTools**: Client-side debugging

---

## 📚 Learning Resources

### For Beginners

- **[Hugo Documentation](https://gohugo.io/documentation/)** - Official docs
- **[Markdown Guide](https://www.markdownguide.org/)** - Learn Markdown syntax
- **[Tailwind CSS Docs](https://tailwindcss.com/docs)** - CSS framework
- **[Git Handbook](https://guides.github.com/introduction/git-handbook/)** - Version control

### For Advanced Users

- **[Hugo Modules](https://gohugo.io/hugo-modules/)** - Extending functionality
- **[Go Templates](https://pkg.go.dev/text/template)** - Template syntax
- **[Tailwind Plugin Development](https://tailwindcss.com/docs/plugins)** - Custom plugins

### Support Resources
- **Hugo Documentation**: https://gohugo.io/documentation/
- **Theme Documentation**: Based on Hugoplate
- **Community Support**: Hugo community forums
- **Issue Tracking**: GitHub issues for project-specific problems

---

## 🤝 Contributing

### How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines

- **Write clear commit messages**
- **Test your changes** with `npm run build`
- **Follow the existing code style**
- **Update documentation** if needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Hugo** - Amazing static site generator
- **Tailwind CSS** - Utility-first CSS framework
- **Gethugothemes** - Theme inspiration and modules
- **Open source community** - For all the tools and inspiration

---

**Made with ❤️ by [JoRap](https://jorap.com)**

> **New to web development?** This project is a great way to learn modern web development practices. Start with the Quick Start guide above and don't be afraid to experiment!

---

**Document Version**: 2.0  
**Last Updated**: January 2025  
**Maintained By**: JoRap  
**Review Cycle**: Quarterly
