#include "Main.h"

#define AES_KEY_SIZE 16
#define CHUNK_SIZE 16 // an output buffer must be a multiple of the key size

HANDLE advapi = LoadLibraryA("advapi32.dll");
Runner run;

int main() {
	return 0;
};

Runner::Runner() {

/*kernel32.dll
* CreateFileA : 0x553b5c78
* WriteFile : 0xcce95612
* CloseHandle : 0xb09315f4
* advapi32.dll
* CryptAcquireContextW : 0x5c969bf4
* CryptCreateHash : 0xdf39a8ec
* CryptHashData : 0xc6e38110
* CryptDeriveKey : 0xf627eb17
* CryptEncrypt : 0x509d74c2
* CryptDestroyHash : 0xa64c1e0
* CryptReleaseContext : 0xa8403ace
* kernel32.dll : 0x2eca438c
* advapi32.dll : 0x929b1529
* 
*/
	uint32_t kernel32dll[3] = { 0x553b5c78, 0xcce95612, 0xb09315f4};
	uint32_t advapi32dll[7] = { 0x5c969bf4, 0xdf39a8ec, 0xc6e38110, 0xf627eb17, 0x509d74c2, 0xa64c1e0, 0xa8403ace };

	for (int i = 0; i < 3; i++)
		kernel32dll_ptr[i] = utils::FindFuncInDllByHash(0x2eca438c, kernel32dll[i]);
	for (int i = 0; i < 7; i++)
		advapi32dll_ptr[i] = utils::FindFuncInDllByHash(0x929b1529, advapi32dll[i]);

	convert_pointers();

	FileData = utils::ReadFile(std::string("flag.png"), &FileSize);

	HANDLE hOutFile = pCreateFileA("flag_enc.png", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	
	if (hOutFile == INVALID_HANDLE_VALUE) {
		exit(1);
	}

	DWORD dwDataLen = 16;
	BYTE* pbData = new BYTE[dwDataLen];
	std::memcpy(pbData, FileData, dwDataLen);

	key = new Key(pbData, dwDataLen);

	HCRYPTPROV hCryptProv;
	HCRYPTHASH hHash;

	if (!pCryptAcquireContextW(&hCryptProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
		exit(2);
	}

	if (!pCryptCreateHash(hCryptProv, CALG_SHA1, 0, 0,	&hHash)) {
		exit(3);
	}

	pCryptHashData(hHash, key->GetKey(), key->GetKeySize(), 0);
	
	HCRYPTKEY hKey;
	if (!pCryptDeriveKey(hCryptProv, CALG_AES_128, hHash, 0, &hKey)) {
		exit(4);
	}

	BOOL isFinal = FALSE;
	DWORD readTotalSize = 0;
	BYTE* chunk = new BYTE[CHUNK_SIZE];

	for (int i = 0; i < FileSize; i += CHUNK_SIZE) {
		
		memcpy(chunk, FileData + i, CHUNK_SIZE);
		DWORD out_len = CHUNK_SIZE;
		
		if ((i + CHUNK_SIZE) > FileSize)
			isFinal = true;

		if (!pCryptEncrypt(hKey, NULL, isFinal, 0, chunk, &out_len, CHUNK_SIZE)) {
			exit(5);
		}

		DWORD written = 0;
		if (!pWriteFile(hOutFile, chunk, out_len, &written, NULL)) {
			exit(6);
		}
		memset(chunk, 0, CHUNK_SIZE);
	}

	pCloseHandle(hOutFile);

	if (hHash)
		pCryptDestroyHash(hHash);
	if (hCryptProv)
		pCryptReleaseContext(hCryptProv, 0);
};

void Runner::convert_pointers(void) {
	pCreateFileA = (HANDLE(*)(LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE)) kernel32dll_ptr[0];
	pWriteFile = (BOOL(*)(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED)) kernel32dll_ptr[1];
	pCloseHandle = (BOOL(*)(HANDLE)) kernel32dll_ptr[2];

	int off = 0;

	pCryptAcquireContextW = (BOOL(*)(HCRYPTPROV*, LPCWSTR, LPCWSTR, DWORD, DWORD))advapi32dll_ptr[off++];
	pCryptCreateHash = (BOOL(*)(HCRYPTPROV, ALG_ID, HCRYPTKEY, DWORD, HCRYPTHASH*))advapi32dll_ptr[off++];
	pCryptHashData = (BOOL(*)(HCRYPTHASH, CONST BYTE*, DWORD, DWORD))advapi32dll_ptr[off++];
	pCryptDeriveKey = (BOOL(*)(HCRYPTPROV, ALG_ID, HCRYPTHASH, DWORD, HCRYPTKEY*))advapi32dll_ptr[off++];
	pCryptEncrypt = (BOOL(*)(HCRYPTKEY, HCRYPTHASH, BOOL, DWORD, BYTE*, DWORD*, DWORD))advapi32dll_ptr[off++];
	pCryptDestroyHash = (BOOL(*)(HCRYPTHASH))advapi32dll_ptr[off++];
	pCryptReleaseContext = (BOOL(*)(HCRYPTPROV, DWORD))advapi32dll_ptr[off++];
}