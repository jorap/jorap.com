---
title: "How I Built JoRap's World"
meta_title: "How I Built JoRap's World: A Guide to Creating a Free Website"
description: "A simple guide to building a website with Hugo and hosting it for free."
slug: "how-i-built-joraps-world"
date: 2024-06-14T05:00:00Z
image: "/images/joraps-world.jpg"
categories: ["Sample"]
author: "John Doe"
tags: ["Website Building", "Free Hosting", "Hugo CMS"]
draft: false
---

## Introduction

So, you want to know how I built "JoRap's World"? It was actually pretty simple once I decided to use Hugo, a static site generator, and host it for free using Cloudflare Pages. Let me walk you through the steps I took to set it all up.

## The Setup

I used to have a site built on Drupal, but I lost my hosting for it. This made me look for a more affordable and reliable solution to keep my site up and running. After searching around, I decided to use Hugo to build the site and Cloudflare Pages for hosting. Both are free and easy to use, making them perfect for my needs.

### Hugo: The Site Generator

First, I needed a way to build my website. After a bit of research, I found Hugo, a tool that lets you create static websites. Static websites are simple, fast, and don't require databases, which makes them a great option for smaller projects.

Hugo uses templates and markdown files, which means that you can write your content in a straightforward, easy-to-read format, and Hugo takes care of the rest. I didn't need to worry about complicated themes or layouts—there are plenty of free templates that you can customize.

### Cloudflare Pages: Free Hosting

Once the site was ready, the next step was hosting. I didn't want to spend money on hosting, so I looked for a free option. That's when I found Cloudflare Pages. It's a platform that lets you deploy static websites without any cost. It connects seamlessly with GitHub, and once you push your code to GitHub, Cloudflare Pages takes care of the rest.

The best part? You don't need to worry about servers or databases—it's all taken care of automatically, and your site is super fast.

## Building the Site

Here's how I built the site:

1. **Set up Hugo**: I started by installing Hugo and setting up a new project. This was just a matter of downloading the software and creating a new site with a simple command.

2. **Choose a Template**: After that, I picked a template for the site. Hugo has a lot of free templates, so I just picked one that I liked, and it was ready to go.

3. **Write Content**: The content is written in markdown files, which are easy to manage. I just created pages for things like blog posts, about me, and the homepage.

4. **Set Up Cloudflare Pages**: Once I had the site ready, I connected it to GitHub and set up Cloudflare Pages to automatically deploy my site every time I made a change. This process was really simple, and Cloudflare did all the hard work.

5. **Add Customization**: I didn't need a lot of custom features, but I did make a few tweaks to the template to fit my needs. This included changing colors and fonts, and adding some personal touches to the layout.

## Going Live

Once everything was set up, I pushed the code to GitHub, and Cloudflare Pages automatically built and deployed my site. In just a few minutes, my website was live and ready to go.

## Conclusion

That's it! I built and hosted my site for free with Hugo and Cloudflare Pages. It was a really straightforward process, and I didn't need to worry about managing hosting or paying for expensive services. Whether you're looking to create a simple personal site or a blog, this setup is perfect for getting started without breaking the bank.

---

I hope this gives you a good overview of how I built the site. Feel free to reach out if you have any questions or want more details!

# How I Built JoRap's World: A Simple Guide to Creating a Static Website with Hugo and Cloudflare Pages

## Introduction: The Journey Begins

A while ago, I realized I needed a website for my personal projects—something easy to manage, cost-effective, and simple to update. I had used Drupal for previous projects, but it just felt like overkill for what I wanted. The hosting was cumbersome, and I didn't need all the bells and whistles a dynamic site offered. After a bit of frustration, I decided to switch to something much simpler: Hugo, a static site generator, combined with Cloudflare Pages for free hosting.

In this guide, I'll show you exactly how I built **JoRap's World**, a simple personal website, using these tools. If you're looking for a straightforward, hassle-free way to create and host your own website without worrying about servers or databases, this guide is for you!

---

## The Setup: Why Hugo and Cloudflare Pages?

Switching from Drupal to Hugo was one of the best decisions I made. Why? Because Hugo is fast, easy to use, and doesn't require much technical knowledge. Plus, Cloudflare Pages is free and super easy to use. Together, they make creating and hosting a personal website or blog as simple as can be.

With these tools, you don't need to worry about back-end infrastructure or expensive hosting services. Everything is static, meaning there's no need for a database or complex server setup. You can focus on your content, and let the tools handle the rest.

---

## Hugo: The Site Generator

### What is Hugo?

Hugo is a **static site generator**—that means it creates websites that don't need a database to work. All the content you create is saved as simple text files (written in **Markdown**) that Hugo turns into web pages. It takes care of the layout, design, and navigation, all based on templates you choose or customize.

The beauty of Hugo is in its simplicity:

* **Templates**: Pre-made designs that you can modify to fit your needs.
* **Markdown Files**: Simple text files where you write your content. These files are easy to edit, and you don't need to learn complicated code to make changes.

### Why Hugo for Small Projects?

Hugo is ideal for small websites because:

* It's **fast**—both to set up and to load for your visitors.
* It's **easy to use**—you don't need to know programming to get started.
* It's **free**—open-source and doesn't require hosting with high fees.

---

## Cloudflare Pages: Free Hosting

### What is Static Website Hosting?

Unlike traditional websites that run on servers with databases, **static websites** are made of simple files—HTML, CSS, and JavaScript—that can be served directly to visitors. This makes them extremely fast and easy to host.

Cloudflare Pages offers **free hosting** for static websites, which is perfect for small personal websites like JoRap's World. With Cloudflare, you can automatically deploy your site from **GitHub**, and they handle everything else.

### Setting Up Cloudflare Pages

1. **Create a Cloudflare Account**: Head to [Cloudflare Pages](https://pages.cloudflare.com) and sign up.
2. **Connect to GitHub**: Link your GitHub account to Cloudflare Pages. This will allow you to deploy your site directly from GitHub, without needing to upload files manually.
3. **Create a New Project**: After connecting GitHub, create a new project in Cloudflare Pages. You'll be able to choose which repository (project) to deploy.

---

## Building the Site: Step-by-Step Process

### 1. Set Up Hugo and Create a New Project

First, you need to install Hugo on your computer. Don't worry, it's simple! Here's how:

* **Install Hugo**: Go to [Hugo's website](https://gohugo.io/getting-started/installing/) and follow the instructions for your operating system (Windows, Mac, Linux).
* **Create a New Site**: Once installed, open your terminal (command line) and type the following:

  ```bash
  hugo new site jorap-world
  ```

  This will create a new Hugo project called "jorap-world" (you can choose any name you like).

### 2. Choose a Template

Hugo comes with free templates you can use to give your site a professional look right away. Here's how to choose and apply one:

* Browse Hugo's [themes page](https://themes.gohugo.io) and find one you like.
* Follow the theme's installation instructions. This typically involves cloning the theme's GitHub repository into your project's `themes` folder.

### 3. Write Content Using Markdown

Now that your site is set up, it's time to add some content. Hugo uses **Markdown**, a simple text-based format for writing content.

* Go to the `content` folder in your Hugo project and create a new file (e.g., `about.md` for your About page).
* Add the following to the file:

  ```markdown
  ---
  title: "About"
  date: 2025-05-11
  ---

  Welcome to JoRap's World! This is a simple website built using Hugo and Cloudflare Pages.
  ```

  Hugo will automatically turn this into a web page with the title "About" and the content you wrote.

### 4. Set Up Cloudflare Pages for Deployment

1. **Push Your Code to GitHub**: Once you're happy with your site, push your Hugo project to a GitHub repository.
2. **Deploy to Cloudflare Pages**: Head to your Cloudflare Pages dashboard, connect your GitHub repo, and select the Hugo project. Cloudflare will automatically deploy your site for you, and your site will be live in minutes.

### 5. Customize the Layout and Design

You can customize your site's layout by editing the theme's settings. This could include changing colors, fonts, or even adding your own logos and images.

* Edit the `config.toml` file in the root of your Hugo project to adjust settings like the title of your site, logo, and theme options.
* If you want to go deeper, you can edit the templates in the `themes` folder or create your own.

---

## Going Live: The Final Step

Once you've finished setting up your site and pushing your code to GitHub, Cloudflare Pages will take care of the rest. It automatically deploys your site and gives you a URL to share with the world. You'll see your site go live within minutes!

---

## Conclusion: A Simple, Free Website

Building **JoRap's World** with Hugo and hosting it for free on Cloudflare Pages was an absolute breeze. The whole process was straightforward, quick, and affordable.

Now that you have the steps, I encourage you to try building your own site using Hugo and Cloudflare Pages. Whether it's for a personal blog, portfolio, or any other project, these tools are perfect for beginners and offer a simple, no-fuss way to go live.

Happy building!

---

### Additional Resources:

* **Hugo Documentation**: [https://gohugo.io/documentation/](https://gohugo.io/documentation/)
* **Cloudflare Pages Setup**: [https://developers.cloudflare.com/pages/](https://developers.cloudflare.com/pages/)
