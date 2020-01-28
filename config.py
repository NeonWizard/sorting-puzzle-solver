colorMap = {
	"red": 0x0,
	"orange": 0x1,
	"yellow": 0x2,
	"ygreen": 0x3,
	"green": 0x4,
	"aqua": 0x5,
	"blue": 0x6,
	"purple": 0x7,
	"pink": 0x8,
	"gray": 0x9,
	"brown": 0xa
}
for x in list(colorMap): colorMap[colorMap[x]] = x # two way map