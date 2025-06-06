module.exports = {
  presence: {
    status: "online",
    activities: [{ name: "Chilling on" }],
  },
  embed: {
    color: 0x4169e1,
  },
  bannerURL: "https://cdn.discordapp.com/attachments/1370391460574400655/1370392743041564683/GGNext.jpg?ex=681f5532&is=681e03b2&hm=e817dafc6bfd1cca86c7436e21107576d2fac19e02dc13d4c2bf404e398cd678&",
  moderation: {
    modRoleId: "1332589809742643200",
    logChannelId: "1368320469731905666",
  },
  queue: {
    defaultMMR: 833,
    mmrGain: 25,
    queueTypes: ["AUScrim", "NAScrim", "BRScrim", "EUScrim", "SGScrim"],
    voiceChannelIds: {
      NAScrim: "1368441003291181056",
      BRScrim: "1368441708211343440",
      SGScrim: "1368440679507951757",
      EUScrim: "1368441771251470497",
      AUScrim: "1368307501564563669",
    },
    lobbyChannelId: "1368300555679825972",
    proofChannelId: "1368307293409509518",
  },
  tournament: {
    formats: ["single", "double", "round-robin"],
    defaultTeamSize: 5,
    checkinWindowMinutes: 60,
    adminRoleId: "1332589809742643200",
  },
  automod: {
    logChannelId: "1368320469731905666",
    antiLinks: {
      enabled: true,
      excludedChannels: [],
      excludedRoles: [],
      excludedLinks: ["example.com", "mywebsite.org"],
    },
    antiInvites: {
      enabled: true,
      excludedChannels: [],
      excludedRoles: [],
    },
    antiBannedWords: {
      enabled: true,
      words: ["fuck", "shit", "cunt", "nigga", "rape"],
      excludedChannels: [],
      excludedRoles: [],
    },
    antiCaps: {
      enabled: true,
      threshold: 0.7,
      excludedChannels: [],
      excludedRoles: [],
    },
  },
};
