# JoRap.com System Specification Documentation

## 1. System Overview

### 1.1 Project Information
- **Project Name**: JoRap's World
- **Website URL**: https://jorap.com
- **System Type**: Static Site Generator (Hugo-based)
- **Current Version**: 2.1.2
- **License**: MIT
- **Author**: JoRap
- **Description**: Personal blog and portfolio website sharing insights on technology, productivity, and life experiences

### 1.2 System Purpose
JoRap.com is a content-focused personal website built to:
- Share blog posts and articles on various topics
- Showcase personal projects and experiences
- Provide a professional online presence
- Deliver fast, SEO-optimized content to visitors

## 2. Technical Architecture

### 2.1 Core Technology Stack
- **Static Site Generator**: Hugo (v0.141.0 minimum)
- **CSS Framework**: Tailwind CSS (v4.1.4)
- **JavaScript Build Tools**: Node.js/npm
- **Go Version**: 1.21+ (for Hugo modules)
- **Template Engine**: Hugo's Go-based templating
- **Content Format**: Markdown with YAML frontmatter

### 2.2 System Dependencies

#### Core Dependencies
```toml
Hugo: v0.141.0+
Go: v1.21+
Node.js: Latest LTS
npm: Latest stable
```

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

### 2.3 System Architecture Components

#### Frontend Components
- **Theme System**: Custom "jorap" theme based on Hugoplate
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark Mode**: System/user preference with theme switcher
- **Search Functionality**: Built-in search with indexed content
- **Image Processing**: Hugo's built-in image processing with WebP support

#### Content Management
- **Content Types**: Blog posts, pages, authors
- **Taxonomies**: Categories and tags
- **Multi-language Support**: English (default), extensible
- **Content Structure**: Organized by content type and language

## 3. File System Structure

### 3.1 Root Directory Structure
```
jorap.com/
├── assets/                 # Static assets (CSS, JS, images)
├── config/                 # Hugo configuration files
├── content/                # Markdown content files
├── data/                   # Data files (JSON/YAML)
├── layouts/                # HTML templates (in theme)
├── static/                 # Static files served as-is
├── themes/jorap/           # Custom theme files
├── scripts/                # Build and maintenance scripts
└── public/                 # Generated static site (build output)
```

### 3.2 Configuration Structure
```
config/
├── _default/
│   ├── hugo.toml          # Main configuration
│   ├── params.toml        # Site parameters
│   ├── menus.en.toml      # Navigation menus
│   ├── languages.toml     # Language settings
│   └── module.toml        # Hugo modules
└── development/
    └── server.toml        # Development server settings
```

### 3.3 Content Organization
```
content/english/
├── _index.md              # Homepage content
├── about/                 # About pages
├── blog/                  # Blog posts
├── authors/               # Author profiles
├── contact/               # Contact information
├── pages/                 # Static pages
└── sections/              # Reusable content sections
```

## 4. System Configuration

### 4.1 Hugo Configuration (`hugo.toml`)
- **Base URL**: Configurable (default: "/")
- **Title**: "JoRap's World"
- **Theme**: "jorap"
- **Timezone**: Asia/Manila
- **Default Language**: English
- **Summary Length**: 10 words
- **Permalink Structure**: Custom for pages
- **Pagination**: 10 items per page

### 4.2 Site Parameters (`params.toml`)
- **Logo**: Custom JoRap logo (60px x 60px)
- **Theme Switcher**: Enabled (light/dark/system)
- **Search**: Enabled with full-text search
- **SEO**: Comprehensive meta tags and OpenGraph
- **Analytics**: Google Analytics ready
- **Social Sharing**: Enabled
- **Cookie Consent**: Configurable

### 4.3 Content Features
- **Blog System**: Full-featured blogging with categories/tags
- **Author Profiles**: Multi-author support
- **Image Optimization**: Automatic WebP conversion
- **Table of Contents**: Auto-generated for long content
- **Syntax Highlighting**: Monokai theme
- **Social Sharing**: Built-in sharing buttons
- **RSS Feeds**: Auto-generated feeds

## 5. User Interface Specifications

### 5.1 Design System
- **CSS Framework**: Tailwind CSS 4.1.4
- **Typography**: System fonts with fallbacks
- **Color Scheme**: Adaptive (light/dark mode)
- **Responsive Breakpoints**: Mobile-first design
- **Icons**: Font Awesome 6 (brands, solid, icons)

### 5.2 Navigation Structure
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

### 5.3 Page Types
- **Homepage**: Banner, features, call-to-action
- **Blog List**: Paginated blog post listings
- **Blog Single**: Individual blog post with sharing
- **About**: Personal information and bio
- **Categories/Tags**: Taxonomy listings
- **Contact**: Contact form and information
- **404**: Custom error page

## 6. Build System

### 6.1 Build Process
```bash
# Development
npm run dev                 # Start development server
npm run preview            # Preview production build
npm run watch              # Watch mode with minification

# Production
npm run build              # Full production build
npm run update-modules     # Update Hugo modules
```

### 6.2 Build Pipeline
1. **Pre-build**: Clear modules, update dependencies
2. **Asset Processing**: Compile CSS, optimize images
3. **Content Processing**: Render Markdown to HTML
4. **Optimization**: Minify HTML/CSS/JS, generate manifests
5. **Output**: Static files in `/public` directory

### 6.3 Build Optimization
- **Template Metrics**: Performance monitoring enabled
- **Asset Minification**: CSS/JS minification in production
- **Image Processing**: WebP conversion, responsive images
- **Caching**: Built-in caching for assets and images (720h)
- **Build Statistics**: Enabled for performance analysis

## 7. Deployment Architecture

### 7.1 Multi-Platform Deployment Support

#### AWS Amplify (`amplify.yml`)
- **Hugo Version**: 0.141.0
- **Go Version**: 1.23.3
- **Build Command**: `npm run project-setup && npm run build`
- **Output Directory**: `/public`
- **Cache**: Node modules

#### Netlify (`netlify.toml`)
- **Hugo Version**: 0.146.5
- **Go Version**: 1.24.2
- **Build Command**: `yarn project-setup; yarn build`
- **Publish Directory**: `public`

#### Vercel (`vercel.json`)
- **Build Script**: `vercel-build.sh`
- **Static Build**: `@vercel/static-build`
- **Output Directory**: `public`
- **404 Handling**: Custom 404.html

### 7.2 CDN and Performance
- **Static Assets**: Served via CDN
- **Image Optimization**: Automatic format conversion
- **Caching Strategy**: Long-term caching for assets
- **Compression**: Gzip enabled

## 8. Security Specifications

### 8.1 Content Security
- **Markdown Rendering**: Safe HTML rendering with goldmark
- **User Input**: Contact forms via external services
- **XSS Protection**: Built-in Hugo protections
- **HTTPS**: Enforced on all platforms

### 8.2 Privacy and Compliance
- **Cookie Consent**: Configurable cookie banner
- **Analytics**: Privacy-focused implementation
- **Data Collection**: Minimal user data collection
- **GDPR**: Cookie consent and privacy policy ready

## 9. Performance Specifications

### 9.1 Performance Targets
- **Google PageSpeed Score**: 95+
- **Core Web Vitals**: Optimized for all metrics
- **Time to First Byte**: <200ms
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s

### 9.2 Optimization Features
- **Static Generation**: Pre-built HTML pages
- **Image Optimization**: WebP conversion, lazy loading
- **Asset Minification**: CSS/JS minification
- **Caching**: Browser and CDN caching
- **Tree Shaking**: Unused CSS/JS removal

## 10. SEO and Analytics

### 10.1 SEO Features
- **Meta Tags**: Comprehensive meta tag support
- **OpenGraph**: Social media sharing optimization
- **Twitter Cards**: Twitter-specific metadata
- **Structured Data**: JSON-LD support
- **Sitemap**: Auto-generated XML sitemap
- **Robots.txt**: Search engine directives

### 10.2 Analytics Integration
- **Google Analytics**: GA4 support (configurable)
- **Google Tag Manager**: GTM integration ready
- **Search Console**: Site verification support
- **Custom Tracking**: Event tracking capabilities

## 11. Content Management

### 11.1 Content Creation Workflow
1. **Write**: Create Markdown files with YAML frontmatter
2. **Organize**: Place in appropriate content directories
3. **Preview**: Use development server for preview
4. **Publish**: Commit to Git, automatic deployment

### 11.2 Content Types and Fields

#### Blog Posts
```yaml
---
title: "Post Title"
description: "Post description"
date: 2024-01-01T00:00:00Z
author: "Author Name"
categories: ["Category"]
tags: ["tag1", "tag2"]
image: "/images/post-image.jpg"
draft: false
---
```

#### Authors
```yaml
---
title: "Author Name"
email: "author@email.com"
image: "/images/author.jpg"
description: "Author bio"
social:
  - name: "twitter"
    icon: "fab fa-twitter"
    link: "https://twitter.com/username"
---
```

## 12. Maintenance and Operations

### 12.1 Regular Maintenance Tasks
- **Dependency Updates**: Monthly Hugo and npm package updates
- **Content Backup**: Regular content repository backups
- **Performance Monitoring**: Monthly performance audits
- **Security Updates**: Apply security patches promptly
- **Link Checking**: Quarterly broken link audits

### 12.2 Monitoring and Logging
- **Build Monitoring**: Deployment status tracking
- **Performance Monitoring**: Core Web Vitals tracking
- **Error Monitoring**: 404 and error page tracking
- **Analytics Review**: Monthly traffic and engagement review

### 12.3 Backup and Recovery
- **Source Code**: Git repository with remote backups
- **Content**: Version-controlled Markdown files
- **Configuration**: All settings in version control
- **Recovery Time**: <30 minutes for full site restore

## 13. Development Workflow

### 13.1 Local Development Setup
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

### 13.2 Development Commands
```bash
npm run dev              # Development server
npm run build            # Production build
npm run preview          # Preview production build
npm run update-modules   # Update Hugo modules
npm run format           # Format code with Prettier
npm run theme-setup      # Set up theme
npm run project-setup    # Project initialization
```

### 13.3 Code Quality
- **Prettier**: Code formatting for consistent style
- **Hugo Linting**: Template and configuration validation
- **Accessibility**: WCAG 2.1 compliance target
- **Performance**: Regular Core Web Vitals auditing

## 14. Extensibility and Customization

### 14.1 Theme Customization
- **CSS Customization**: Tailwind CSS configuration
- **Layout Overrides**: Template customization in themes/
- **Component Addition**: Custom Hugo shortcodes
- **JavaScript Enhancement**: Custom JS in assets/

### 14.2 Content Extension
- **New Content Types**: Add new archetypes
- **Custom Fields**: Extend frontmatter schemas
- **Taxonomies**: Add new classification systems
- **Multilingual**: Add new language support

### 14.3 Feature Addition
- **Hugo Modules**: Extend with additional modules
- **Third-party Services**: API integrations
- **Custom Shortcodes**: Reusable content components
- **Plugin System**: Via Hugo modules ecosystem

## 15. System Requirements

### 15.1 Development Environment
- **Operating System**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Node.js**: 16+ LTS
- **Go**: 1.21+
- **Hugo**: 0.141.0+ (extended version)
- **Git**: 2.20+

### 15.2 Production Environment
- **Hosting**: Static hosting (Netlify, Vercel, AWS Amplify)
- **CDN**: Automatic via hosting platform
- **SSL**: Automatic certificate management
- **Domain**: Custom domain support

### 15.3 Browser Support
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Android 90+
- **Graceful Degradation**: Basic functionality on older browsers

## 16. Troubleshooting and Support

### 16.1 Common Issues
- **Build Failures**: Check Hugo/Go versions, clear modules
- **Asset Issues**: Verify Tailwind CSS compilation
- **Content Issues**: Validate frontmatter YAML syntax
- **Performance Issues**: Audit image sizes and quantities

### 16.2 Debugging Tools
- **Hugo Server**: Development server with live reload
- **Template Metrics**: Performance debugging
- **Build Statistics**: Asset analysis
- **Browser DevTools**: Client-side debugging

### 16.3 Support Resources
- **Hugo Documentation**: https://gohugo.io/documentation/
- **Theme Documentation**: Based on Hugoplate
- **Community Support**: Hugo community forums
- **Issue Tracking**: GitHub issues for project-specific problems

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Maintained By**: JoRap  
**Review Cycle**: Quarterly 