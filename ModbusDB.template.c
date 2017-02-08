//------------------------------------------------------------------------
// DO NOT EDIT - Auto generated code
//------------------------------------------------------------------------
#include "Modbus/ModbusTypes.h"
#include "Core/App.h"

extern version_t 		M3_version;
extern version_t 		FPGA_version;
extern app_settings_t   Settings;
extern app_t  			Measurements;

/* ----------------------------------------------------------------	*/

const MBVAR_RECORD_T mbtable[] =
{
	// TODO: Codegen ARM modbus
	// 4000-4999 Reserved for ARM
	{4000, 2, RO, &(M3_version.Dirty)},
	{4002, 2, RO, &(M3_version.Hash)},
	{4004, 2, RO, &(M3_version.Major)},
	{4006, 2, RO, &(M3_version.Minor)},
	{4008, 2, RO, &(M3_version.Subversion)},

	{4020, 2, RO, &(FPGA_version.Dirty)},
	{4022, 2, RO, &(FPGA_version.Hash)},
	{4024, 2, RO, &(FPGA_version.Major)},
	{4026, 2, RO, &(FPGA_version.Minor)},
	{4028, 2, RO, &(FPGA_version.Subversion)},

	// 5000- DSP code-generated modbus
[tpl]	{$address, $length, $access, &($varname)},
[/tpl]};

/* ----------------------------------------------------------------	*/

uint16_t ModbusDB_NrOfEntries(void)
{
	return NUM_ELEMS(mbtable);
}

/* ----------------------------------------------------------------	*/