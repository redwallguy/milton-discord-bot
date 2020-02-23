import * as dotenv from "dotenv";
dotenv.config();

import * as Discord from "discord.js";
import * as fs from "fs";

const client = new Discord.Client();
client.commands = new Discord.Collection();
const prefix = process.env.DISCORD_PREFIX;
const commandFiles = fs.readdirSync('./build/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(`./commands/${file}`); // using dynamic import for consistency is impractical
	client.commands.set(command.name, command);
}

client.once('ready', () => {
	console.log('Ready!');
});

client.on('message', message => {
    if (!message.content.startsWith(prefix) || message.author.bot) return;

	const args = message.content.slice(prefix.length).split(/ +/);
	const command = args.shift().toLowerCase();

	if (!client.commands.has(command)) return;

	try {
		client.commands.get(command).execute(message, args);
	} catch (error) {
		console.error(error);
		message.reply('there was an error trying to execute that command!');
	}
});

client.login(process.env.DISCORD_TOKEN);
