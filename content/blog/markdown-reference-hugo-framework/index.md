---
title: "Markdown Reference for HUGO Framework"
date: 2019-05-12
image: "blog/images/markdown.jpg"
description: "Markdown Reference for HUGO CMS Users."
---

[Basic Syntax](https://www.markdownguide.org/basic-syntax)  
[Extended Syntax](https://www.markdownguide.org/extended-syntax)

## Headers
---
**Markdown**

```markdown
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```

**Output**

# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6

## Emphasis
---
**Markdown**

```markdown
*Italics (Emphasis)* uses 1 asterisk. Add 2 spaces for a line break.  
**Bold (Strong)** uses 2 asterisks. Add 2 spaces for a line break.    
***Bold (Strong) and Italics (Emphasis)*** uses 3 asterisks. No spaces for a new paragraph.

_Italics (Emphasis)_ uses 1 underscore.  Add 2 spaces for a line break.  
__Bold (Strong)__ uses 2 underscores.  Add 2 spaces for a line break.  
___Bold (Strong) and Italics (Emphasis)___ uses 3 underscores. No spaces for a new paragraph.
```

**Output**

*Italics (Emphasis)* uses 1 asterisk. Add 2 spaces for a line break.  
**Bold (Strong)** uses 2 asterisks. Add 2 spaces for a line break.    
***Bold (Strong) and Italics (Emphasis)*** uses 3 asterisks. No spaces for a new paragraph.

_Italics (Emphasis)_ uses 1 underscore.  Add 2 spaces for a line break.  
__Bold (Strong)__ uses 2 underscores.  Add 2 spaces for a line break.  
___Bold (Strong) and Italics (Emphasis)___ uses 3 underscores. No spaces for a new paragraph.

## Blockquotes
---
**Markdown**
```markdown
> To create a blockquote, add a > in front of a paragraph.  
> Blockquotes can contain multiple paragraphs.  
> **Markdown**
> 
> Add a > on the blank lines between the paragraphs.
> 
>> Blockquotes can be nested.  
>> Add a >> in front of the paragraph you want to nest.
```

**Output**

> To create a blockquote, add a > in front of a paragraph.  
> Blockquotes can contain multiple paragraphs.  
> **Markdown**
> 
> Add a > on the blank lines between the paragraphs.
> 
>> Blockquotes can be nested.  
>> Add a >> in front of the paragraph you want to nest.

## Lists
---
**Markdown**
```markdown
1. Ordered List
2. Ordered List
3. Ordered List

- Unordered List
- Unordered List
- Unordered List

1. Ordered List
   - Add 3 spaces for 1st level sub items
   - Add 3 spaces for 1st level sub items
1. Ordered List
   - Add 3 spaces for 1st level sub items
   - Add 3 spaces for 1st level sub items
1. Ordered List  
    Preserve the list by indent the element **four spaces**
   - Add 3 spaces for 1st level sub items  
      Preserve the list by indenting the element **six spaces**
   - Add 3 spaces for 1st level sub items
```

**Output**

1. Ordered List
2. Ordered List
3. Ordered List

- Unordered List
- Unordered List
- Unordered List

1. Ordered List
   - Add 3 spaces for 1st level sub items
   - Add 3 spaces for 1st level sub items
1. Ordered List
   - Add 3 spaces for 1st level sub items
   - Add 3 spaces for 1st level sub items
1. Ordered List. Add 2 spaces for a line break.  
    Preserve the list by indent the element **four spaces**
   - Add 3 spaces for 1st level sub items. Add 2 spaces for a line break.  
      Preserve the list by indenting the element **six spaces**
   - Add 3 spaces for 1st level sub items

## Section
---
**Markdown**

**Output**
