# JoRap.com - Personal Blog and Portfolio Website

<p align="center">
  <img src="assets/images/logo.png" alt="JoRap's World Logo" width="120" height="120">
</p>

<p align="center">
  <strong>A modern, fast, and SEO-optimized personal website built with Hugo and Tailwind CSS</strong>
</p>

<p align="center">
  <a href="https://jorap.com">🌐 Live Website</a> | 
  <a href="#quick-start">🚀 Quick Start</a> | 
  <a href="#development-guide">👨‍💻 Development Guide</a>
</p>

---

## 📋 Table of Contents

1. [What is JoRap.com?](#what-is-jorapcom)
2. [Quick Start Guide](#quick-start)
3. [Understanding the Project](#understanding-the-project)
4. [Development Guide](#development-guide)
5. [Configuration & Customization](#configuration--customization)
6. [Content Management](#content-management)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Features](#advanced-features)
10. [Contributing](#contributing)

---

## 🌟 What is JoRap.com?

JoRap.com is a personal blog and portfolio website that showcases:

- **Blog posts** about technology, productivity, and life experiences
- **Personal projects** and professional work
- **Resources and tutorials** for developers and tech enthusiasts

### 🛠️ Built With

- **[Hugo](https://gohugo.io/)** - Static site generator (super fast!)
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Go](https://golang.org/)** - Programming language (used by Hugo)
- **[Node.js](https://nodejs.org/)** - JavaScript runtime (for build tools)

### ✨ Key Features

- 🚀 **Lightning Fast** - Static site generation means super fast loading
- 📱 **Mobile Responsive** - Looks great on all devices
- 🌙 **Dark Mode** - Automatic theme switching
- 🔍 **Search Function** - Find content easily
- 📊 **SEO Optimized** - Google-friendly structure
- 🏷️ **Tags & Categories** - Organized content
- 👥 **Multi-Author Support** - Multiple writers can contribute
- 📝 **Markdown Content** - Easy content creation
- 🎨 **Customizable** - Easy to modify and extend

---

## 🚀 Quick Start

### Prerequisites (What You Need First)

Before you start, make sure you have these installed on your computer:

1. **Hugo Extended** v0.141.0 or higher
   - Download from: https://gohugo.io/installation/
   - ⚠️ **Important**: Get the "extended" version, not the regular one

2. **Node.js** v16 or higher
   - Download from: https://nodejs.org/
   - This includes npm (Node Package Manager)

3. **Go** v1.21 or higher
   - Download from: https://golang.org/dl/
   - Required for Hugo modules

4. **Git** (for version control)
   - Download from: https://git-scm.com/

### Step-by-Step Setup

1. **Download the project**
   ```bash
   git clone https://github.com/yourusername/jorap.com.git
   cd jorap.com
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up the project structure**
   ```bash
   npm run project-setup
   ```
   > This script sets up the Hugo theme and moves files to the right places

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   - Go to `http://localhost:1313`
   - You should see the website running! 🎉

---

## 📁 Understanding the Project

### Project Structure Explained

```
jorap.com/
├── assets/              # Images, CSS, JS files
├── config/              # Website settings
├── content/             # Your blog posts and pages (Markdown files)
├── data/                # Site data (JSON files)
├── scripts/             # Helper scripts for development
├── static/              # Files served as-is (robots.txt, etc.)
├── themes/jorap/        # The website theme (design and layout)
├── hugo.toml           # Main configuration file
├── package.json        # Node.js dependencies and scripts
└── README.md           # This file!
```

### Important Files for Beginners

- **`hugo.toml`** - Main settings (site title, URL, etc.)
- **`package.json`** - Lists all the tools and commands available
- **`content/english/`** - Where your blog posts and pages live
- **`config/_default/params.toml`** - Website appearance settings
- **`data/theme.json`** - Colors and fonts

### Content Organization

```
content/english/
├── _index.md           # Homepage content
├── about/              # About page
├── blog/               # Blog posts go here
├── authors/            # Author profiles
├── contact/            # Contact page
└── pages/              # Other static pages
```

---

## 👨‍💻 Development Guide

### Available Commands

Here are all the commands you can use (run with `npm run`):

```bash
# Development Commands
npm run dev              # Start development server (most common)
npm run build            # Build for production
npm run preview          # Preview production build locally

# Setup Commands
npm run project-setup    # Initial project setup
npm run update-modules   # Update Hugo modules
npm run format           # Format code with Prettier

# Theme Commands
npm run theme-setup      # Set up theme
npm run update-theme     # Update theme to latest version
npm run remove-darkmode  # Remove dark mode feature
```

### Development Workflow

1. **Start the development server**
   ```bash
   npm run dev
   ```

2. **Make changes** to your content or code

3. **See changes live** - The browser will automatically refresh

4. **Build for production** when ready
   ```bash
   npm run build
   ```

### Understanding Hugo Basics

Hugo is a **static site generator**. This means:

- You write content in **Markdown** (easy text format)
- Hugo converts it to **HTML** (web pages)
- No database needed - everything is files!

**Example Markdown:**
```markdown
---
title: "My First Blog Post"
date: 2024-01-01
author: "Your Name"
---

# Hello World!

This is my first blog post. I can use **bold** and *italic* text.

- List item 1
- List item 2
```

---

## ⚙️ Configuration & Customization

### Basic Site Settings

Edit `hugo.toml` to change basic settings:

```toml
# Change these to match your site
baseURL = "https://yoursite.com"
title = "Your Site Title"
```

### Site Parameters

Edit `config/_default/params.toml` for advanced settings:

```toml
# Site branding
logo = "images/logo.png"
logo_darkmode = "images/logo-dark.png"
favicon = "images/favicon.png"

# Features
search = true
cookie_consent = true
```

### Customizing Colors and Fonts

Edit `data/theme.json`:

```json
{
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#1E40AF"
  },
  "fonts": {
    "primary": "Inter, sans-serif"
  }
}
```

### Adding Social Links

Edit `data/social.json`:

```json
[
  {
    "name": "Twitter",
    "icon": "fab fa-twitter",
    "link": "https://twitter.com/yourusername"
  },
  {
    "name": "GitHub",
    "icon": "fab fa-github",
    "link": "https://github.com/yourusername"
  }
]
```

---

## 📝 Content Management

### Creating a New Blog Post

1. **Create a new file** in `content/english/blog/`
2. **Name it** something like `my-awesome-post.md`
3. **Add frontmatter** (metadata) at the top:

```markdown
---
title: "My Awesome Post"
description: "A short description of your post"
date: 2024-01-01T10:00:00Z
author: "Your Name"
categories: ["Technology"]
tags: ["Hugo", "Web Development"]
image: "images/my-post-image.jpg"
draft: false
---

# Your Post Content Goes Here

Write your blog post using Markdown syntax.
```

### Frontmatter Fields Explained

- **`title`** - The post title (required)
- **`description`** - SEO description (shows in search results)
- **`date`** - Publication date (ISO format)
- **`author`** - Author name (must match author in `authors/`)
- **`categories`** - Main topic categories
- **`tags`** - Specific tags for the post
- **`image`** - Featured image path
- **`draft`** - Set to `true` to hide from public site

### Adding Images

1. **Add images** to `assets/images/`
2. **Reference them** in your content:
   ```markdown
   ![Alt text](images/my-image.jpg)
   ```

### Creating Author Profiles

1. **Create a file** in `content/english/authors/`
2. **Add author information**:

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
---

Extended bio content here...
```

---

## 🚀 Deployment

### Supported Platforms

The site is configured to deploy on:

- **[Netlify](https://netlify.com)** - Easy drag-and-drop deployment
- **[Vercel](https://vercel.com)** - Git-based deployment
- **[AWS Amplify](https://aws.amazon.com/amplify/)** - Amazon's hosting service
- **[GitHub Pages](https://pages.github.com)** - Free hosting for open source

### Quick Deployment Guide

#### Option 1: Netlify (Recommended for Beginners)

1. **Build your site**
   ```bash
   npm run build
   ```

2. **Drag the `public` folder** to netlify.com

3. **Your site is live!** 🎉

#### Option 2: Vercel

1. **Push your code** to GitHub
2. **Connect** your GitHub repo to Vercel
3. **Auto-deployment** happens on every push

#### Option 3: Custom Server

1. **Build the site**
   ```bash
   npm run build
   ```

2. **Upload the `public` folder** to your web server

### Important Deployment Notes

- **Always run `npm run build`** before deploying
- **Update `baseURL`** in `hugo.toml` to match your domain
- **Test locally** with `npm run preview` before deploying

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "Hugo not found" Error

**Problem**: Hugo isn't installed or not in PATH
**Solution**: 
- Install Hugo Extended from https://gohugo.io/installation/
- Make sure it's the "extended" version
- Restart your terminal

#### 2. "Module not found" Error

**Problem**: Hugo modules aren't initialized
**Solution**:
```bash
npm run update-modules
```

#### 3. Styles Not Loading

**Problem**: Tailwind CSS isn't compiling
**Solution**:
```bash
npm install
npm run dev
```

#### 4. Images Not Showing

**Problem**: Wrong image paths
**Solution**:
- Check image path in your markdown
- Ensure images are in `assets/images/`
- Use relative paths: `images/my-image.jpg`

#### 5. Build Fails

**Problem**: Various build issues
**Solution**:
```bash
# Clear everything and start fresh
rm -rf node_modules
rm -rf resources
npm install
npm run update-modules
npm run build
```

### Getting Help

If you're stuck:

1. **Check the error message** - it often tells you exactly what's wrong
2. **Search Google** for the error message
3. **Ask on Hugo forums** - https://discourse.gohugo.io/
4. **Check Hugo documentation** - https://gohugo.io/documentation/

---

## 🚀 Advanced Features

### Performance Optimization

The site includes several performance features:

- **Image optimization** - Automatic WebP conversion
- **Code minification** - Smaller file sizes
- **Caching** - Faster subsequent loads
- **CDN support** - Global content delivery

### SEO Features

- **Automatic sitemaps** - Help search engines index your site
- **Meta tags** - Proper SEO metadata
- **OpenGraph tags** - Better social media sharing
- **JSON-LD structured data** - Rich search results

### Analytics Integration

Add Google Analytics by updating `hugo.toml`:

```toml
[services.googleAnalytics]
ID = 'G-MEASUREMENT_ID'
```

### Custom Shortcodes

Create reusable content snippets:

```markdown
{{< youtube "video-id" >}}
{{< spotify "track-id" >}}
```

### Multilingual Support

Add support for multiple languages by:

1. **Creating language files** in `content/[language]/`
2. **Updating** `config/_default/languages.toml`
3. **Adding translations** in `i18n/`

---

## 🤝 Contributing

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
   ```bash
   npm run dev
   npm run build
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Code Style Guidelines

- **Use Prettier** for formatting: `npm run format`
- **Write descriptive commit messages**
- **Test your changes** before submitting
- **Update documentation** if needed

---

## 📚 Learning Resources

### For Beginners

- **Markdown Guide** - https://markdownguide.org/
- **Hugo Quick Start** - https://gohugo.io/getting-started/quick-start/
- **Git Tutorial** - https://git-scm.com/docs/gittutorial

### For Advanced Users

- **Hugo Documentation** - https://gohugo.io/documentation/
- **Tailwind CSS Docs** - https://tailwindcss.com/docs
- **Go Templates** - https://gohugo.io/templates/introduction/

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Hugo](https://gohugo.io/)** - Amazing static site generator
- **[Tailwind CSS](https://tailwindcss.com/)** - Fantastic CSS framework
- **[Hugoplate](https://github.com/zeon-studio/hugoplate)** - Base theme
- **[Zeon Studio](https://zeon.studio/)** - Original theme creators

---

## 📞 Support

If you need help:

- **Read this documentation** first
- **Check the [troubleshooting section](#troubleshooting)**
- **Open an issue** on GitHub
- **Contact** via the website contact form

---

<p align="center">
  Made with ❤️ by JoRap | 
  <a href="https://jorap.com">Visit Website</a>
</p>
