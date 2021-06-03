#define MPU6050_ADDR 			0x68
#define WHO_AM_I_REG 			0x75
#define PWR_MGMT_1_REG 		0x6B
#define SMPLRT_DIV_REG 		0x19
#define GYRO_CONFIG_REG 	0x1B
#define ACCEL_CONFIG_REG 	0x1C
#define ACCEL_XOUT_H_REG 	0x3B
#define GYRO_XOUT_H_REG 	0x43
#define TEMP_OUT_H_REG 		0x41


#include "main.h"

bool initMPU6050(void);
void readData(uint16_t *data, uint8_t dataType);
