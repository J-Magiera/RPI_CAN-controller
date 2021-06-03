/**
  ******************************************************************************
  * @file    usart.c
  * @brief   This file provides code for the configuration
  *          of the USART instances.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "usart.h"
#include "string.h"

/* USER CODE BEGIN 0 */
static uint8_t lenOfNumber(uint16_t num);
/* USER CODE END 0 */

UART_HandleTypeDef huart1;

/* USART1 init function */

void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

void HAL_UART_MspInit(UART_HandleTypeDef* uartHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(uartHandle->Instance==USART1)
  {
  /* USER CODE BEGIN USART1_MspInit 0 */

  /* USER CODE END USART1_MspInit 0 */
    /* USART1 clock enable */
    __HAL_RCC_USART1_CLK_ENABLE();

    __HAL_RCC_GPIOA_CLK_ENABLE();
    /**USART1 GPIO Configuration
    PA9     ------> USART1_TX
    PA10     ------> USART1_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_9|GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* USER CODE BEGIN USART1_MspInit 1 */

  /* USER CODE END USART1_MspInit 1 */
  }
}

void HAL_UART_MspDeInit(UART_HandleTypeDef* uartHandle)
{

  if(uartHandle->Instance==USART1)
  {
  /* USER CODE BEGIN USART1_MspDeInit 0 */

  /* USER CODE END USART1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART1_CLK_DISABLE();

    /**USART1 GPIO Configuration
    PA9     ------> USART1_TX
    PA10     ------> USART1_RX
    */
    HAL_GPIO_DeInit(GPIOA, GPIO_PIN_9|GPIO_PIN_10);

  /* USER CODE BEGIN USART1_MspDeInit 1 */

  /* USER CODE END USART1_MspDeInit 1 */
  }
}


void numToUart(uint16_t num)
{
	uint8_t count = lenOfNumber(num);
	uint8_t numToSend = 0;
	switch (count)
	{	
		case 5:
			numToSend = num/10000 + NumOffset;
			HAL_UART_Transmit(&huart1, &numToSend, sizeof(numToSend),20);
		case 4:
			num = num % 10000;
			numToSend = num/1000 + NumOffset;
			HAL_UART_Transmit(&huart1, &numToSend, sizeof(numToSend),20);
		case 3:
			num = num % 1000;
			numToSend = num/100 + NumOffset;
			HAL_UART_Transmit(&huart1, &numToSend, sizeof(numToSend),20);
		case 2:
			num = num % 100;
			numToSend = num/10 + NumOffset;
			HAL_UART_Transmit(&huart1, &numToSend, sizeof(numToSend),20);
		case 1:
			num = num % 10;
			numToSend = num/1 + NumOffset;
			HAL_UART_Transmit(&huart1, &numToSend, sizeof(numToSend),20);
			SEND_NEW_LINE;
			break;
		default:
			HAL_UART_Transmit(&huart1, (uint8_t*)"Not recognite digit", strlen("Not recognite digit"),20);
			SEND_NEW_LINE;
	}

}

static uint8_t lenOfNumber(uint16_t num)
{	
	uint8_t count = 0;
	
	while(0 != num)
	{
		num /=10;
		count++;
	}
	
	return count;
}


/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
