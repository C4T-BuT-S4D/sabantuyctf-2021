#include <cstdint>
#include <vector>
#include <Windows.h>
#include <Wincrypt.h>
#include <iostream>
#include <string>
#include <fstream>
#include <cwctype>
#include <algorithm>

#define CHUNK_SIZE 16
uint8_t* ReadFile(std::string filename, size_t* outSize);

int main() {
	size_t size = 0;
    uint8_t* data = ReadFile(std::string("flag_enc.png"), &size);

    uint8_t key[16] = { 0x89, 0x50, 0x4E, 0x47, 0xD, 0xA, 0x1A, 0xA, 0x0, 0x0, 0x0, 0xD, 0x49, 0x48, 0x44, 0x52 };
    for (int i = 0; i < 16; i++) {
        key[i] ^= 0x42;
    }

	HANDLE hOutFile = CreateFileA("flag_dec.png", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

	if (hOutFile == INVALID_HANDLE_VALUE) {
		exit(1);
	}

	HCRYPTPROV hCryptProv;
	HCRYPTHASH hHash;

	if (!CryptAcquireContextW(&hCryptProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
		exit(2);
	}

	if (!CryptCreateHash(hCryptProv, CALG_SHA1, 0, 0, &hHash)) {
		exit(3);
	}

	CryptHashData(hHash, key, 16, 0);

	HCRYPTKEY hKey;
	if (!CryptDeriveKey(hCryptProv, CALG_AES_128, hHash, 0, &hKey)) {
		exit(4);
	}

	BOOL isFinal = FALSE;
	DWORD readTotalSize = 0;
	BYTE* chunk = new BYTE[CHUNK_SIZE];

	for (int i = 0; i < size; i += CHUNK_SIZE) {

		memcpy(chunk, data + i, CHUNK_SIZE);
		DWORD out_len = CHUNK_SIZE;

		if ((i + CHUNK_SIZE) > size)
			isFinal = true;

		if (!CryptDecrypt(hKey, NULL, isFinal, 0, chunk, &out_len)) {
			exit(5);
		}

		DWORD written = 0;
		if (!WriteFile(hOutFile, chunk, out_len, &written, NULL)) {
			exit(6);
		}
		memset(chunk, 0, CHUNK_SIZE);
	}

	CloseHandle(hOutFile);

	if (hHash)
		CryptDestroyHash(hHash);
	if (hCryptProv)
		CryptReleaseContext(hCryptProv, 0);

	return 0;
}

uint8_t* ReadFile(std::string filename, size_t* outSize)
{
    std::ifstream file(filename, std::ios::binary);

    if (!file.is_open()) {
        exit(1337);
    }

    file.unsetf(std::ios::skipws);
    std::streampos fileSize;

    file.seekg(0, std::ios::end);
    fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    std::vector<uint8_t> tmpData;
    tmpData.reserve(fileSize);

    tmpData.insert(tmpData.begin(),
        std::istream_iterator<uint8_t>(file),
        std::istream_iterator<uint8_t>()
    );

    uint8_t* out = new uint8_t[tmpData.size()];
    *outSize = tmpData.size();
    for (int i = 0; i < tmpData.size(); i++)
    {
        out[i] = tmpData[i];
    }

    return out;
};