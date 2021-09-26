#include "utils.h"

void utils::crc32(const void* data, size_t n_bytes, uint32_t* crc) {
    uint32_t table[0x100];
    for (size_t i = 0; i < 0x100; ++i)
        table[i] = crc32_for_byte(i);
    for (size_t i = 0; i < n_bytes; ++i)
        *crc = table[(uint8_t)*crc ^ ((uint8_t*)data)[i]] ^ *crc >> 8;
};

uint32_t utils::crc32_for_byte(uint32_t r) {
    for (int j = 0; j < 8; ++j)
        r = (r & 1 ? 0 : (uint32_t)0xEDB88320L) ^ r >> 1;
    return r ^ (uint32_t)0xFF000000L;
}

uint8_t* utils::ReadFile(std::string filename, size_t* outSize)
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

uint64_t utils::bytes2qword(uint8_t* p_data)
{
    uint64_t value = 0;
    value = (uint64_t)p_data[0] << 56;
    value += (uint64_t)p_data[1] << 48;
    value += (uint64_t)p_data[2] << 40;
    value += (uint64_t)p_data[3] << 32;
    value += (uint64_t)p_data[4] << 24;
    value += (uint64_t)p_data[5] << 16;
    value += (uint64_t)p_data[6] << 8;
    value += (uint64_t)p_data[7];
    return value;
};

uint32_t utils::bytes2dword(uint8_t* p_data)
{
    uint32_t value = 0;
    value = p_data[0] << 24;
    value += p_data[1] << 16;
    value += p_data[2] << 8;
    value += p_data[3];
    return value;
};

uint16_t utils::bytes2word(uint8_t* p_data)
{
    uint16_t value = 0;
    value += p_data[0] << 8;
    value += p_data[1];
    return value;
};


uint64_t utils::FindFuncInDllByHash(uint64_t DllHash, uint64_t FuncHash) {
    typedef FARPROC(WINAPI* GetProcAddress_t) (HMODULE, const char*);
    typedef struct _UNICODE_STRING {
        USHORT Length;
        USHORT MaximumLength;
        PWSTR  Buffer;
    } UNICODE_STRING, * PUNICODE_STRING;

    struct LDR_MODULE
    {
        LIST_ENTRY e[3];
        HMODULE    base;
        void* entry;
        UINT       size;
        UNICODE_STRING dllPath;
        UNICODE_STRING dllname;
    };
    int offset = 0x60;
    int ModuleList = 0x18;
    int ModuleListFlink = 0x18;
    int KernelBaseAddr = 0x10;

    INT_PTR peb = __readgsqword(offset);
    INT_PTR mdllist = *(INT_PTR*)(peb + ModuleList);
    INT_PTR mlink = *(INT_PTR*)(mdllist + ModuleListFlink);
    INT_PTR krnbase = *(INT_PTR*)(mlink + KernelBaseAddr);

    LDR_MODULE* mdl = (LDR_MODULE*)mlink;
    bool found = false;
    do
    {
        mdl = (LDR_MODULE*)mdl->e[0].Flink;

        if (mdl->base != NULL)
        {
            int ssize = lstrlenW(mdl->dllname.Buffer);
            std::wstring a(mdl->dllname.Buffer);
            std::transform(
                a.begin(), a.end(),
                a.begin(),
                towlower);

            uint32_t crc = 0;
            crc32((void*)a.c_str(), ssize * 2, &crc);
            //std::wcout << a;
            //std::cout << " : 0x" << std::hex << crc << std::endl;

            if (crc == DllHash) {
                found = true;
                break;
            }
        }
    } while (mlink != (INT_PTR)mdl);

    if (!found)
        return 0;

    found = false;
    HMODULE kernel32base = (HMODULE)mdl->base;
    ULONG_PTR base = (ULONG_PTR)kernel32base;
    IMAGE_NT_HEADERS* pe = PIMAGE_NT_HEADERS(base + PIMAGE_DOS_HEADER(base)->e_lfanew);
    IMAGE_EXPORT_DIRECTORY* exportDir = PIMAGE_EXPORT_DIRECTORY(base + pe->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    int32_t DirCnt = exportDir->NumberOfNames;
    DWORD* namePtr = (DWORD*)(base + exportDir->AddressOfNames); // Адрес имен функций.
    WORD* ordPtr = (WORD*)(base + exportDir->AddressOfNameOrdinals); //Адрес имени для функции.

    for (int i = 0; i < DirCnt; i++) {
        char* ptr = (char*)(base + *namePtr);
        int ssize = strlen(ptr);
        uint32_t crc = 0;
        crc32(ptr, ssize, &crc);
        //std::cout << ptr << " : 0x" << std::hex << crc << std::endl;
        if (crc == FuncHash) {
            found = true;
            break;
        }
        namePtr++;
        ordPtr++;
    }

    if (!found)
        return 0;

    DWORD funcRVA = *(DWORD*)(base + exportDir->AddressOfFunctions + *ordPtr * 4);
    auto funcAddr = (GetProcAddress_t)(base + funcRVA);

    return (uint64_t)funcAddr;
};

uint64_t utils::GetDllNameHash(LPCWSTR name) {
    int StringSize = lstrlenW(name);

    std::cout << StringSize << std::endl;
    uint32_t crc = 0;
    crc32((void*)name, StringSize * 2, &crc);
    return crc;
};