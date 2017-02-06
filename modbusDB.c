// Some comment code. 

void ModBus()
{		

	3000;
	Settings.Major;
	U16;

	3001;
	Settings.Major;
	U16;

	3002;
	process.adc.channel1.value;
	U16;

	3003;
	process.scaleVdc.value;
	F32;

	4000;
	Settings.ScaleVdc.Gain;
	F32;


[tpl]

testing multiple tags
[/tpl]
}
