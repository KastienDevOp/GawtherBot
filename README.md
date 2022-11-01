<a name="#top"></a>

# **_The Gawther Platform_** - **_Discord Extension_**

## Table of Contents

> - [About Gawther](#about-gawther)
> - [About The Team](#about-team)
> - [Gawther's Commands](#bot-commands)
>   - [General Commands](#general-commands)
>   - [Staff Commands](#staff-commands)
>   - [Developer Commands](#dev-commands)
> - [Gawther's Tasks](#task-loops)
>   - [On Member Join](#on-member-join)
>   - [Pending Verification](#pending-verification)
>   - [Check Database For Members](check-db-for-members)


# About Gawther <a name="#about-gawther">📎</a>

Gawther started back in 2019, originally named ButtlerBot. ButtlerBot was going to be the bot that could do anything every other bot can do and more. From bridging various game chats through different socket workings and https calls, to relaying information back and forth between it's website counter-partner and all of it's inclusions. This bot was going to be the brain behind everything, however, as progression continued, we started noticing how limited the [discord api](https://discordpy.readthedocs.io/en/stable/) was eventually ButtlerBot became a stagnant project that is now being converted into Gawther. Gawther's inspiration came from various components of my life. The first component being my immediate surroundings. Starting with my friends. What can discord help me automate for them? Well the major thing being notifications, automated messages for streaming and such, bridged game chats for interactions with discord members who aren't in the game, and a few other things. The second component was what can I create that no one else can. That's the main question every programmer asks themselves. What can I create that can blow the world away?! Well after a while of researching various bots, I noticed that there weren't really a lot of gaming bots. What I mean is bots that actually have games. Not your average Hangman, or CoinFlip, but I'm gearing more towards actual text-based [RPG's](https://www.techopedia.com/definition/27052/role-playing-game-rpg). Although there are other contributing components to the creation of Gawther, those are the two main driving points.

# About The Team <a name="#about-team">📎</a>

The team is currently comprised of only Kas and myself. We have slots available for anyone who'd like to become one of Gawther's Developers, but for now it's just an interview-styled conversation with Kas and me. In the future, I do plan to build a web-based application along with a text-based application through Gawther.

## Mek

With having such a wide-scaled scheme of what I wanted my bot to achieve, I realized I had bit off more than I could chew as I took zero time to study the Python langauge inside and out and just jumped straight into learning a few basics and then running away with the documentation (which I had zero clue on how to read) which explains why there are so many different versions and re-writes to ButtlerBot as I was not only learning the language, but learning how to read documentation as well as doing other side projects (oooh squirrel moments) and could just never sit down and focus long enough to complete a project.  

You can find my very first repository [here](https://github.com/shellbyy0124?tab=repositories) which contains all the projects I have started and never completed (or trashed). If you'd like more direct links, see below. As you digress through the repository, you'll see 1) numerous re-writes of the bot, and the incorporation of other projects as I started to branch out into other languages and projects. As you hover over each link, a hinting window will show up explaining each repo and a description of what the repository is about.

> - [Main Repo](https://github.com/shellbyy0124?tab=repositories) - When I was working under the Shellbyy alias
>   - [python-speaks](https://github.com/shellbyy0124/python-speaks, "Learning To Make My Computer Talk")
>   - [random-project-generator](https://github.com/shellbyy0124/random-project-generator, "At this point I had become bored and was tired of trying to think of a project on my own thus I started looking to various difficulty leveled projects and built a program to generate a project for me based off inserted criteria.")
>   - [Gawther-Bot](https://github.com/shellbyy0124/Gawther-Bot, "This was going to be the first official version of Gawther, but I decided to turn it into a playground to see what I could come up with my own from scratch.")
>   - [gawther-discord-bot](https://github.com/shellbyy0124/gawther-discord-bot, "Another version of Gawther. Still tossing around ideas and trying to really get an idea of where I wanted to go with the bot.")
>   - [random-project-generator](https://github.com/shellbyy0124/random_project_generator, "A second version of the first random project generator. This one is a project generator that generates randomly without user input.")
>   - [meks_projects.github.io](https://github.com/shellbyy0124/meks_projects.github.io, "I was learning to build websites and was trying to create a website that would showcase all of my projects I had accomplished. This eventually became trash.")
>   - [create-react-app-in-python](https://github.com/shellbyy0124/create-react-app-in-python, "I honestly got tired of manually creating website workspace projects for each new project everytime I messed one up and had to start over, so I attempted to automize creating the workspace.")
>   - [calculator.github.io](https://github.com/shellbyy0124/calculator.github.io, "I had finally created my first calculator and added a few features for my cousin to use at work.")
>   - [shaans_jewelers](https://github.com/shellbyy0124/shaans_jewelers, "Thought I was good enough with building websites that I could build one for a local jewelery store in town, and then realized just how aggravating the backend work was going to be to learn and trashed the project.")
>   - [gawth3r_platform](https://github.com/shellbyy0124/gawth3r_platform, "The second renaming of the platform. Still trying to figure out a direction to go with the bot.")
>   - [mekasu0124.github.io](https://github.com/shellbyy0124/mekasu0124.github.io, "Second attempt at creating my own website...or my first attempt. Check the dates on which one is most recent. That's the second one :P")
>   - [Gother_discord](https://github.com/shellbyy0124/Gother_discord, "Either another renaming or another idea tossing version of the bot")
>   - [Gother_Discord_Js](https://github.com/shellbyy0124/Gother_Discord_Js, "Attempting to learn the Discord JS Documentation and seeing if I wanted to do the bot in JavaScript instead of Python as I was heavily enjoying JavaScript at the time")
>   - [Gother](https://github.com/shellbyy0124/Gother, "Attempting to bring the two extensions together as one working platform.")
>   - [ButtlerBotDiscord](https://github.com/shellbyy0124/ButtlerBotDiscord, "Another version of ButtlerBot that went more in depth")
>   - [new_bot_code](https://github.com/shellbyy0124/new_bot_code, "I had messed up the current working environment for the bot, and needed a place to host the files while I fixed the environment and switched operating systems.")
>   - [ButtlerBot](https://github.com/shellbyy0124/ButtlerBot, "This repo houses a new version of the bot. I had started working in versions instead of just re-writing the bot over and over.")

> - [Main Repo](https://github.com/mekasu0124?tab=repositories) - Under my new alias of Mekasu
>   - [GawtherBot](, "This is the current running project folder for the Gawther Platform Discord Extension.") Currently Private While In Development. Will Edit With A Link To The Public Version When Available.
>   - [GawtherWebsite](, "This is the current running project folder for the Gawther Platform Website Extension.") Currently Private While In Developement. Will Edit With A Link To The Public Version When Available.
>   - [meks-todo-app](https://github.com/mekasu0124/meks-todo-app, "Started Learning Mobile App Development using the ReactNative framework.")
>   - [meks-address-book](https://github.com/mekasu0124/meks-address-book, "Learned how to create my own address book in Python. Decided to showcase it.")

As you can see, my new repository has drastically increased as with my progression into programming, I've learned more proper setups for various projects, better ways to write the same things. I've learned amazing things programmaticaly such as one-line if-statments, one-line for loops with list comprehension, and more. As someone who learned a couple of basics and then decided to take on the world, I ***highly*** recomment to each new programmer to please take the time to learn the basics. Learn the fundamentals over and over until you can do them in your sleep. Start a Learning folder for yourself where you house all of your tutorials and side projects. When you learn a new concept, go practice it or build a project with it.

## Kas

# Bot Commands <a name="#bot-commands">📎</a>

How To Read Table Below:

> ```
>
> - Command Name
>   - how to execute command
>   - description of the command
>   - restrictions to the command
>
> ```

## General Commands <a name="#general-commands">📎</a>

- **Favorite Quote**
  - /gawther fav_quote
  - Allows a member to set their favorite quote which is currently only used on embed footers that do not have a preset foot note.
  - Must be a printable [string](https://docs.python.org/3/library/string.html)
- **Help**
  - /gawther help
  - Returns a Paginator Embed to the member showing all available commands to them
  - Must have a staff members role in order to see the staff help menu.
  - Must have a developer members role in oder to see the developers help menu.
- **Ping**
  - /gawther ping
  - Return the bots current latency, or the delay before a transfer of data begins following an instruction for its transfer.
  - The latency must be greater-than or equal-to 20 in order for the member to report the latency to the developers.
- **Rules**
  - /gawther rules
  - Returns a Paginator Embed of all the current rules for both the Website and Discord extensions.
  - None
- **Server**
  - /gawther server
  - Returns a Paginator Embed displaying various counts, status', roles, people in roles, and more
  - None
- **Solved**
  - /gawther solved
  - Marks a support forum thread within the Support category in the Discord Extension as solved which therein closes the channel, writes the messages within the support channel to a text document format in memory and sends the file with a confirmation embed to their direct messages.
  - Must be in a Support Thread within the Support Category to use this command.
- **Subscribe**
  - /gawther subscribe
  - Returns a link to the Website Extension that allows a member to sign-up for and subscribe to the Gather Platform. Once available, furthering details will be shown here.
  - None
- **Who Is**
  - /gawther who_is
  - Requests member input for a user's ID then returns a Paginator Embed showing various details on the target member.
  - The input from the member must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).

## Bank Commands <a name="#bank-commands">📎</a>

- **List Requests**
  - /bank list_requests
  - Returns a Paginator Embed of all open unpaid requests from other members within the discord server.
  - None
- **Pay**
  - /bank pay
  - Requests user input for target member to pay, the amount, and the reason. Pays the member the amount owed (does appropriate addition/subtraction to numbers written in database) and sends a confirmation embed to both users and to a notification channel for staff within the discord server.
  - Member must be either their ID 1234564890123 or their name Gawther
  - Amount must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
  - Reason must be a printable [string](https://docs.python.org/3/library/string.html).
- **Pay Request**
  - /bank pay_request
  - Allows a member to pay a specified request at a time.
  - Target member must be an ID (012345678901234) or name (Gawther)
  - Amount must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
  - Reason must be a printable [string](https://docs.python.org/3/library/string.html).
  - Request Number must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
- **Request**
  - /bank request
  - Allows a member to request money from another member for whatever reason
  - Target member must be an ID (012345678901234) or name (Gawther)
  - Amount must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
  - Reason must be a printable [string](https://docs.python.org/3/library/string.html).

## Staff Commands <a name="#staff-commands">📎</a>

- **Adjust Balance**
  - /bank adjust_balance
  - Allows a staff member to adjust a members balance. The amount given to the member is subtracted from the guilds bank alotment. The amount taken from the member is added to the guilds bank alotment.
  - Target member must be an ID (012345678901234) or name (Gawther)
  - Amount must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
  - Reason must be a printable [string](https://docs.python.org/3/library/string.html).
- **Purge**
  - /staff purge
  - Allows a staff member to purge *n* messages from the channel the command is executed in, then produces a file from temporary memory to the designated notification channel.
  - Amount must be an [Integer](https://www.w3schools.com/python/python_numbers.asp#:~:text=Int%2C%20or%20integer%2C%20is%20a%20whole%20number%2C%20positive%20or%20negative%2C%20without%20decimals%2C%20of%20unlimited%20length.) or [Whole Number](https://www.google.com/search?q=definition+of+a+whole+number&client=opera&hs=DFN&sxsrf=ALiCzsZc6JQtSlKhacOplIMiRtX16IM5aQ%3A1667178124225&ei=jB5fY-qgDZSgqtsPhqmmuAs&ved=0ahUKEwjqlvy-oon7AhUUkGoFHYaUCbcQ4dUDCBA&uact=5&oq=definition+of+a+whole+number&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQgAQQRhD5ATIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMggIABAWEB4QDzIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQ1gQQsAM6BwgAELADEEM6CQgjECcQRhD5AToECAAQQzoKCAAQgAQQhwIQFDoICAAQgAQQsQM6BAgjECc6BQgAEJECOg8IABCABBCHAhAUEEYQ-QE6BwgAEIAEEAo6CAgAEBYQHhAKSgQITRgBSgQIQRgASgQIRhgAUPQHWOQbYIgdaAFwAXgAgAGYAYgB9hKSAQQyLjE5mAEAoAEByAEKwAEB&sclient=gws-wiz-serp#:~:text=a%20number%20without%20fractions%3B%20an%20integer.).
  - Reason must be a printable [string](https://docs.python.org/3/library/string.html).

## Developer Commands <a name="#dev-commands">📎</a>

- **Send Developer Note**
  - /developers send_dev_note
  - Allows a developer to send a note to a designated dev_notes channel of any messages they need to leave behind for other developers. When the message is sent, it also pings a silent role named dev_notes to alert other developers of the note.
  - The note must be a printable [string](https://docs.python.org/3/library/string.html).
- **Create Category**
  - /developers create_category
  - As an ever-growing and ever-developing community, this allows the developers to be able to quickly create a new category within the discord. In future updates of the bot, this command will be developed further to allow for *security options* which are different levels of permissions for the various roles within the discord server to have setup autonimously.
  - The category name must be a printable [string](https://docs.python.org/3/library/string.html).
- **Create Channel**
  - /developers create_channel
  - In addition to the **Create Category** command, this command allows developers to swiftly create channels within a category within the discord extension and automatically syncs the channels permissions to that of the parent category. Requests user in put for the channel's name, and category.
  - The channel name and category name must be a printable [string](https://docs.python.org/3/library/string.html).
- **Delete Category**
  - /developers delete_category
  - Allows developers to delete a specified category within the discord server. It requests user input on what to do with any channels that are in the category currently with the options to delete or move them. 
  - User inputs must be a printable [string](https://docs.python.org/3/library/string.html).
- **Delete Channel**
  - /developers delete_channel
  - Allows developers to delete a specified channel within a specified category. It requests user input on creating a backup of the entire channel or not.
  - User inputs must be a printable [string](https://docs.python.org/3/library/string.html).

# Gawther's Tasks <a name="#task-loops">📎</a>

Gawther is also comprised of a number of task loops that majorly assist in language filters, bridge chat re-connections, and more.

## On Member Join <a name="#on-member-join">📎</a>

This function activates when a member joins the discord by sending the user a welcome embed. Within this embed, we display our values, missions, rules, and punishment table. The embed may seem a bit overwhelming as we are currently debating on a proper approach for this welcome message, but it also selects a random quote to display on the welcome embed that is sent to the designated welcome channel within the discord server. In addition, it also writes the new member to the database (or picks back up where the member left off if it's a returning member) with a fresh bank amount of $1,000 GB. The GB stands for Gawther Bucks.

## Check Pending <a name="#pending-verification">📎</a>

This task loop runs every 24 hours and checks for any members who have created their accounts on the [discord main website](https://discord.com) but never verified their accounts through their email, or for whatever reason. If there are any members with a true pending status will be courtesly notified by the bot that their pending verification. Anyone who does not go and verify their account with 72 hours of receiving the first message, then they will be removed from the discord server as a safety precaution.

## Check Database For Members <a name="#check-db-for-members">📎</a>

This task loop runs every 12 hours and just runs a double check that any and all members who have joined Gawther within the last 12 hours are written to the database. It's a secondary check for just in case a member joins the channel and send Confirm to the bot when the bot DM's them, but it gives them an error message. The staff members will have a command that will write the new member to the database so that the member does not have to wait until the 12-hour mark for the bot to write them to the database.


[Top](#top)