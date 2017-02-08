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
	{5000, 2, RO, &(Measurements.faultlogic.activeFaults)},
	{5002, 2, RO, &(Measurements.faultlogic.enableOutput)},
	{5004, 2, RO, &(Measurements.faultlogic.faultInputs)},
	{5006, 2, RO, &(Measurements.faultlogic.faultPresent)},
	{5008, 2, RO, &(Measurements.faultlogic.pendingCommands)},
	{5010, 2, RO, &(Measurements.faultlogic.tripFault)},
	{5012, 2, RO, &(Measurements.samples.IdcSample1)},
	{5014, 2, RO, &(Measurements.samples.VacSample2.R)},
	{5016, 2, RO, &(Measurements.samples.VacSample2.S)},
	{5018, 2, RO, &(Measurements.samples.VacSample2.T)},
	{5020, 2, RO, &(Measurements.samples.VdcSample)},
	{5022, 2, RW, &(Settings.Buttons.ratioValues)},
	{5024, 2, RW, &(Settings.Buttons.tableLength)},
	{5026, 2, RW, &(Settings.Buttons.tolerance)},
	{5028, 2, RW, &(Settings.Version.Dirty)},
	{5030, 2, RW, &(Settings.Version.Hash)},
	{5032, 2, RW, &(Settings.Version.Major)},
	{5034, 2, RW, &(Settings.Version.Minor)},
	{5036, 2, RW, &(Settings.Version.Subversion)},
	{5038, 2, RW, &(Settings.checksum)},
};

/* ----------------------------------------------------------------	*/

uint16_t ModbusDB_NrOfEntries(void)
{
	return NUM_ELEMS(mbtable);
}

/* ----------------------------------------------------------------	*/