#include "stdafx.h"
#include <audioenginebaseapo.h>
#include <baseaudioprocessingobject.h>
#include <memory.h>

// APO GUID
static const GUID CLSID_BlackfoxCustomAPO = 
{ 0xa1b2c3d4, 0xe5f6, 0x4789, { 0xab, 0xcd, 0xef, 0x12, 0x34, 0x56, 0x78, 0x90 } };

class BlackfoxCustomAPO : public CBaseAudioProcessingObject
{
public:
    // Remove "= default" and declare it properly
    BlackfoxCustomAPO() {}     // empty constructor

    DECLARE_APO_COM_CLASS();   // Very important Microsoft macro
    STDMETHODIMP GetRegistrationProperties(APO_REG_PROPERTIES** ppRegProps) override
    {
        if (!ppRegProps) return E_POINTER;

        *ppRegProps = (APO_REG_PROPERTIES*)CoTaskMemAlloc(sizeof(APO_REG_PROPERTIES) + sizeof(GUID));
        if (!*ppRegProps) return E_OUTOFMEMORY;

        ZeroMemory(*ppRegProps, sizeof(APO_REG_PROPERTIES) + sizeof(GUID));

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

    // === CORRECT signatures (this was the main error) ===
    STDMETHODIMP IsInputFormatSupported(
        IAudioMediaType* pOppositeFormat,
        IAudioMediaType* pRequestedInputFormat,
        IAudioMediaType** ppSupportedInputFormat) override
    {
        *ppSupportedInputFormat = pRequestedInputFormat;
        if (pRequestedInputFormat) pRequestedInputFormat->AddRef();
        return S_OK;
    }

    STDMETHODIMP IsOutputFormatSupported(
        IAudioMediaType* pOppositeFormat,
        IAudioMediaType* pRequestedOutputFormat,
        IAudioMediaType** ppSupportedOutputFormat) override
    {
        *ppSupportedOutputFormat = pRequestedOutputFormat;
        if (pRequestedOutputFormat) pRequestedOutputFormat->AddRef();
        return S_OK;
    }

    STDMETHODIMP_(void) APOProcess(
        UINT32 u32NumInputConnections,
        APO_CONNECTION_PROPERTY** ppInputConnections,
        UINT32 u32NumOutputConnections,
        APO_CONNECTION_PROPERTY** ppOutputConnections) override
    {
        if (u32NumInputConnections == 0 || u32NumOutputConnections == 0) return;

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

        // Pass-through (identity)
        CopyMemory(pOutput->pBuffer, pInput->pBuffer, 
                   (size_t)pInput->u32ValidFrameCount * 8);  // 2 channels * 4 bytes float

        pOutput->u32ValidFrameCount = pInput->u32ValidFrameCount;
        pOutput->u32BufferFlags     = pInput->u32BufferFlags;
    }
};

__declspec(dllexport) CBaseAudioProcessingObject* __cdecl CreateBlackfoxCustomAPO()
{
    return new BlackfoxCustomAPO();
}