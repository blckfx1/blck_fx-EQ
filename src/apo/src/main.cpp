#include <windows.h>
#include <AudioEngineBaseAPO.h>

static const GUID CLSID_BlackfoxCustomAPO = 
{ 0xa1b2c3d4, 0xe5f6, 0x4789, { 0xab, 0xcd, 0xef, 0x12, 0x34, 0x56, 0x78, 0x90 } };

class BlackfoxCustomAPO : public CBaseAudioProcessingObject
{
public:
    BlackfoxCustomAPO() = default;

    STDMETHODIMP GetRegistrationProperties(APO_REG_PROPERTIES** ppRegProps) override
    {
        if (!ppRegProps) return E_POINTER;

        *ppRegProps = (APO_REG_PROPERTIES*)CoTaskMemAlloc(sizeof(APO_REG_PROPERTIES));
        if (!*ppRegProps) return E_OUTOFMEMORY;

        ZeroMemory(*ppRegProps, sizeof(APO_REG_PROPERTIES));

        APO_REG_PROPERTIES* pProps = *ppRegProps;
        pProps->clsid = CLSID_BlackfoxCustomAPO;
        pProps->Flags = APO_FLAG_DEFAULT;
        pProps->u32MinInputConnections  = 1;
        pProps->u32MaxInputConnections  = 1;
        pProps->u32MinOutputConnections = 1;
        pProps->u32MaxOutputConnections = 1;

        wcscpy_s(pProps->szFriendlyName, L"blackfoxCustomAPO");
        wcscpy_s(pProps->szCopyrightInfo, L"© 2026 Justin - blck_fx-eq");

        return S_OK;
    }

    STDMETHODIMP IsInputFormatSupported(IAudioMediaType* pProposedInputFormat,
                                       IAudioMediaType** ppSupportedInputFormat) override
    {
        *ppSupportedInputFormat = pProposedInputFormat;
        if (pProposedInputFormat) pProposedInputFormat->AddRef();
        return S_OK;
    }

    STDMETHODIMP IsOutputFormatSupported(IAudioMediaType* pProposedOutputFormat,
                                        IAudioMediaType** ppSupportedOutputFormat) override
    {
        *ppSupportedOutputFormat = pProposedOutputFormat;
        if (pProposedOutputFormat) pProposedOutputFormat->AddRef();
        return S_OK;
    }

    STDMETHODIMP_(void) APOProcess(
        UINT32 u32NumInputConnections,
        APO_CONNECTION_PROPERTY** ppInputConnections,
        UINT32 u32NumOutputConnections,
        APO_CONNECTION_PROPERTY** ppOutputConnections) override
    {
        UNREFERENCED_PARAMETER(u32NumInputConnections);
        UNREFERENCED_PARAMETER(u32NumOutputConnections);

        APO_CONNECTION_PROPERTY* pInput  = ppInputConnections[0];
        APO_CONNECTION_PROPERTY* pOutput = ppOutputConnections[0];

        if (pInput->u32ValidFrameCount == 0)
        {
            pOutput->u32ValidFrameCount = 0;
            return;
        }

        if (pInput->u32BufferFlags == BUFFER_SILENT)
        {
            pOutput->u32BufferFlags = BUFFER_SILENT;
            pOutput->u32ValidFrameCount = pInput->u32ValidFrameCount;
            return;
        }

        FLOAT32* pSrc = (FLOAT32*)pInput->pBuffer;
        FLOAT32* pDst = (FLOAT32*)pOutput->pBuffer;

        CopyMemory(pDst, pSrc, (size_t)pInput->u32ValidFrameCount * 8); // stereo float32

        pOutput->u32ValidFrameCount = pInput->u32ValidFrameCount;
        pOutput->u32BufferFlags     = pInput->u32BufferFlags;
    }
};

__declspec(dllexport) CBaseAudioProcessingObject* __cdecl CreateBlackfoxCustomAPO()
{
    return new BlackfoxCustomAPO();
}