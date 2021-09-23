#pragma once

#include <cstdint>
#include <string>
#include <fstream>
#include <vector>
#include <Windows.h>
#include <iostream>
#include <cwctype>
#include <algorithm>

namespace utils
{
	uint32_t crc32_for_byte(uint32_t r);
	void crc32(const void* data, size_t n_bytes, uint32_t* crc);
	uint8_t* ReadFile(std::string filename, size_t* outSize);

	uint64_t bytes2qword(uint8_t* p_data);
	uint32_t bytes2dword(uint8_t* p_data);
	uint16_t bytes2word(uint8_t* p_data);
	uint64_t FindFuncInDllByHash(uint64_t, uint64_t);
	uint64_t GetDllNameHash(LPCWSTR name);
};

