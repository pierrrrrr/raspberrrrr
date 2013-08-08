from ctypes import Structure, Union
from ctypes import c_int, c_uint, c_char, c_char_p, c_void_p
from ctypes import cast
from ctypes import POINTER, CFUNCTYPE
from ctypes import CDLL



OMX_VERSION_MAJOR = 1
OMX_VERSION_MINOR = 1
OMX_VERSION_REVISION = 2
OMX_VERSION_STEP = 0
OMX_ALL = 0xffffffff

OMX_VERSION = ((OMX_VERSION_STEP<<24) | (OMX_VERSION_REVISION<<16) | (OMX_VERSION_MINOR<<8) | OMX_VERSION_MAJOR)


(OMX_StateInvalid,
 OMX_StateLoaded,
 OMX_StateIdle,
 OMX_StateExecuting,
 OMX_StatePause,
 OMX_StateWaitForResources) = range(6)

(OMX_CommandStateSet,
 OMX_CommandFlush,
 OMX_CommandPortDisable,
 OMX_CommandPortEnable,
 OMX_CommandMarkBuffer) = range(5)

(OMX_EventCmdComplete,
 OMX_EventError,
 OMX_EventMark,
 OMX_EventPortSettingsChanged,
 OMX_EventBufferFlag,
 OMX_EventResourcesAcquired,
 OMX_EventComponentResumed,
 OMX_EventDynamicResourcesAvailable,
 OMX_EventPortFormatDetected) = range(9)


(OMX_IndexComponentStartUnused,# = 0x01000000,
 OMX_IndexParamPriorityMgmt,
 OMX_IndexParamAudioInit,
 OMX_IndexParamImageInit,
 OMX_IndexParamVideoInit,
 OMX_IndexParamOtherInit,
 OMX_IndexParamNumAvailableStreams,
 OMX_IndexParamActiveStream,
 OMX_IndexParamSuspensionPolicy,
 OMX_IndexParamComponentSuspended,
 OMX_IndexConfigCapturing,
 OMX_IndexConfigCaptureMode,
 OMX_IndexAutoPauseAfterCapture,
 OMX_IndexParamContentURI,
 OMX_IndexParamCustomContentPipe,
 OMX_IndexParamDisableResourceConcealment,
 OMX_IndexConfigMetadataItemCount,
 OMX_IndexConfigContainerNodeCount,
 OMX_IndexConfigMetadataItem,
 OMX_IndexConfigCounterNodeID,
 OMX_IndexParamMetadataFilterType,
 OMX_IndexParamMetadataKeyFilter,
 OMX_IndexConfigPriorityMgmt,
 OMX_IndexParamStandardComponentRole,) = [0x01000000 + i for i in range(24)]

(OMX_IndexPortStartUnused, # = 0x02000000,
 OMX_IndexParamPortDefinition,
 OMX_IndexParamCompBufferSupplier,) = [0x02000000 + i for i in range(3)]

(OMX_IndexReservedStartUnused) = 0x03000000

(OMX_IndexAudioStartUnused, # = 0x04000000,
 OMX_IndexParamAudioPortFormat,
 OMX_IndexParamAudioPcm,
 OMX_IndexParamAudioAac,
 OMX_IndexParamAudioRa,
 OMX_IndexParamAudioMp3,
 OMX_IndexParamAudioAdpcm,
 OMX_IndexParamAudioG723,
 OMX_IndexParamAudioG729,
 OMX_IndexParamAudioAmr,
 OMX_IndexParamAudioWma,
 OMX_IndexParamAudioSbc,
 OMX_IndexParamAudioMidi,
 OMX_IndexParamAudioGsm_FR,
 OMX_IndexParamAudioMidiLoadUserSound,
 OMX_IndexParamAudioG726,
 OMX_IndexParamAudioGsm_EFR,
 OMX_IndexParamAudioGsm_HR,
 OMX_IndexParamAudioPdc_FR,
 OMX_IndexParamAudioPdc_EFR,
 OMX_IndexParamAudioPdc_HR,
 OMX_IndexParamAudioTdma_FR,
 OMX_IndexParamAudioTdma_EFR,
 OMX_IndexParamAudioQcelp8,
 OMX_IndexParamAudioQcelp13,
 OMX_IndexParamAudioEvrc,
 OMX_IndexParamAudioSmv,
 OMX_IndexParamAudioVorbis,
 OMX_IndexConfigAudioMidiImmediateEvent,
 OMX_IndexConfigAudioMidiControl,
 OMX_IndexConfigAudioMidiSoundBankProgram,
 OMX_IndexConfigAudioMidiStatus,
 OMX_IndexConfigAudioMidiMetaEvent,
 OMX_IndexConfigAudioMidiMetaEventData,
 OMX_IndexConfigAudioVolume,
 OMX_IndexConfigAudioBalance,
 OMX_IndexConfigAudioChannelMute,
 OMX_IndexConfigAudioMute,
 OMX_IndexConfigAudioLoudness,
 OMX_IndexConfigAudioEchoCancelation,
 OMX_IndexConfigAudioNoiseReduction,
 OMX_IndexConfigAudioBass,
 OMX_IndexConfigAudioTreble,
 OMX_IndexConfigAudioStereoWidening,
 OMX_IndexConfigAudioChorus,
 OMX_IndexConfigAudioEqualizer,
 OMX_IndexConfigAudioReverberation,
 OMX_IndexConfigAudioChannelVolume,) = [0x04000000 + i for i in range(121-74+1)]

(OMX_IndexImageStartUnused, # = 0x05000000,
 OMX_IndexParamImagePortFormat,
 OMX_IndexParamFlashControl,
 OMX_IndexConfigFocusControl,
 OMX_IndexParamQFactor,
 OMX_IndexParamQuantizationTable,
 OMX_IndexParamHuffmanTable,
 OMX_IndexConfigFlashControl,) = [0x05000000 + i for i in range(8)]

(OMX_IndexVideoStartUnused, # = 0x06000000,
 OMX_IndexParamVideoPortFormat,
 OMX_IndexParamVideoQuantization,
 OMX_IndexParamVideoFastUpdate,
 OMX_IndexParamVideoBitrate,
 OMX_IndexParamVideoMotionVector,
 OMX_IndexParamVideoIntraRefresh,
 OMX_IndexParamVideoErrorCorrection,
 OMX_IndexParamVideoVBSMC,
 OMX_IndexParamVideoMpeg2,
 OMX_IndexParamVideoMpeg4,
 OMX_IndexParamVideoWmv,
 OMX_IndexParamVideoRv,
 OMX_IndexParamVideoAvc,
 OMX_IndexParamVideoH263,
 OMX_IndexParamVideoProfileLevelQuerySupported,
 OMX_IndexParamVideoProfileLevelCurrent,
 OMX_IndexConfigVideoBitrate,
 OMX_IndexConfigVideoFramerate,
 OMX_IndexConfigVideoIntraVOPRefresh,
 OMX_IndexConfigVideoIntraMBRefresh,
 OMX_IndexConfigVideoMBErrorReporting,
 OMX_IndexParamVideoMacroblocksPerFrame,
 OMX_IndexConfigVideoMacroBlockErrorMap,
 OMX_IndexParamVideoSliceFMO,
 OMX_IndexConfigVideoAVCIntraPeriod,
 OMX_IndexConfigVideoNalSize,) = [0x06000000 + i for i in range(161-135+1)]

(OMX_IndexCommonStartUnused, # = 0x07000000,
 OMX_IndexParamCommonDeblocking,
 OMX_IndexParamCommonSensorMode,
 OMX_IndexParamCommonInterleave,
 OMX_IndexConfigCommonColorFormatConversion,
 OMX_IndexConfigCommonScale,
 OMX_IndexConfigCommonImageFilter,
 OMX_IndexConfigCommonColorEnhancement,
 OMX_IndexConfigCommonColorKey,
 OMX_IndexConfigCommonColorBlend,
 OMX_IndexConfigCommonFrameStabilisation,
 OMX_IndexConfigCommonRotate,
 OMX_IndexConfigCommonMirror,
 OMX_IndexConfigCommonOutputPosition,
 OMX_IndexConfigCommonInputCrop,
 OMX_IndexConfigCommonOutputCrop,
 OMX_IndexConfigCommonDigitalZoom,
 OMX_IndexConfigCommonOpticalZoom,
 OMX_IndexConfigCommonWhiteBalance,
 OMX_IndexConfigCommonExposure,
 OMX_IndexConfigCommonContrast,
 OMX_IndexConfigCommonBrightness,
 OMX_IndexConfigCommonBacklight,
 OMX_IndexConfigCommonGamma,
 OMX_IndexConfigCommonSaturation,
 OMX_IndexConfigCommonLightness,
 OMX_IndexConfigCommonExclusionRect,
 OMX_IndexConfigCommonDithering,
 OMX_IndexConfigCommonPlaneBlend,
 OMX_IndexConfigCommonExposureValue,
 OMX_IndexConfigCommonOutputSize,
 OMX_IndexParamCommonExtraQuantData,
 OMX_IndexConfigCommonFocusRegion,
 OMX_IndexConfigCommonFocusStatus,
 OMX_IndexConfigCommonTransitionEffect,) = [0x07000000 + i for i in range(199-165+1)]

(OMX_IndexOtherStartUnused, # = 0x08000000
 OMX_IndexParamOtherPortFormat,
 OMX_IndexConfigOtherPower,
 OMX_IndexConfigOtherStats,) = [0x08000000 + i for i in range(4)]

(OMX_IndexTimeStartUnused, # = 0x09000000
 OMX_IndexConfigTimeScale,
 OMX_IndexConfigTimeClockState,
 OMX_IndexConfigTimeActiveRefClock,
 OMX_IndexConfigTimeCurrentMediaTime,
 OMX_IndexConfigTimeCurrentWallTime,
 OMX_IndexConfigTimeCurrentAudioReference,
 OMX_IndexConfigTimeCurrentVideoReference,
 OMX_IndexConfigTimeMediaTimeRequest,
 OMX_IndexConfigTimeClientStartTime,
 OMX_IndexConfigTimePosition,
 OMX_IndexConfigTimeSeekMode) = [0x09000000 + i for i in range(12)]

(OMX_IndexKhronosExtensions) = 0x6F000000
(OMX_IndexVendorStartUnused) = 0x7F000000

(OMX_TIME_RefClockNone,
 OMX_TIME_RefClockAudio,
 OMX_TIME_RefClockVideo) = range(3)

OMX_BUFFERFLAG_EOS = 0x00000001
OMX_BUFFERFLAG_STARTTIME = 0x00000002
OMX_BUFFERFLAG_DECODEONLY = 0x00000004
OMX_BUFFERFLAG_DATACORRUPT = 0x00000008
OMX_BUFFERFLAG_ENDOFFRAME = 0x00000010
OMX_BUFFERFLAG_SYNCFRAME = 0x00000020
OMX_BUFFERFLAG_EXTRADATA = 0x00000040
OMX_BUFFERFLAG_CODECCONFIG = 0x00000080

OMX_BUFFERFLAG_TIME_UNKNOWN = 0x00000100

(OMX_PortDomainAudio,
 OMX_PortDomainVideo,
 OMX_PortDomainImage,
 OMX_PortDomainOther) = range(4)

OMX_PortDomainKhronosExtensions = 0x6F000000
OMX_PortDomainVendorStartUnused = 0x7F000000
OMX_PortDomainMax = 0x7ffffff

(OMX_IMAGE_CodingUnused,
 OMX_IMAGE_CodingAutoDetect,
 OMX_IMAGE_CodingJPEG,
 OMX_IMAGE_CodingJPEG2K,
 OMX_IMAGE_CodingEXIF,
 OMX_IMAGE_CodingTIFF,
 OMX_IMAGE_CodingGIF,
 OMX_IMAGE_CodingPNG,
 OMX_IMAGE_CodingLZW,
 OMX_IMAGE_CodingBMP) = range(10)

(OMX_VIDEO_CodingUnused,
 OMX_VIDEO_CodingAutoDetect,
 OMX_VIDEO_CodingMPEG2,
 OMX_VIDEO_CodingH263,
 OMX_VIDEO_CodingMPEG4,
 OMX_VIDEO_CodingWMV,
 OMX_VIDEO_CodingRV,
 OMX_VIDEO_CodingAVC,
 OMX_VIDEO_CodingMJPEG,) = range(9)

(OMX_COLOR_FormatUnused,
 OMX_COLOR_FormatMonochrome,
 OMX_COLOR_Format8bitRGB332,
 OMX_COLOR_Format12bitRGB444,
 OMX_COLOR_Format16bitARGB4444,
 OMX_COLOR_Format16bitARGB1555,
 OMX_COLOR_Format16bitRGB565,
 OMX_COLOR_Format16bitBGR565,
 OMX_COLOR_Format18bitRGB666,
 OMX_COLOR_Format18bitARGB1665,
 OMX_COLOR_Format19bitARGB1666,
 OMX_COLOR_Format24bitRGB888,
 OMX_COLOR_Format24bitBGR888,
 OMX_COLOR_Format24bitARGB1887,
 OMX_COLOR_Format25bitARGB1888,
 OMX_COLOR_Format32bitBGRA8888,
 OMX_COLOR_Format32bitARGB8888,
 OMX_COLOR_FormatYUV411Planar,
 OMX_COLOR_FormatYUV411PackedPlanar,
 OMX_COLOR_FormatYUV420Planar,
 OMX_COLOR_FormatYUV420PackedPlanar,
 OMX_COLOR_FormatYUV420SemiPlanar,
 OMX_COLOR_FormatYUV422Planar,
 OMX_COLOR_FormatYUV422PackedPlanar,
 OMX_COLOR_FormatYUV422SemiPlanar,
 OMX_COLOR_FormatYCbYCr,
 OMX_COLOR_FormatYCrYCb,
 OMX_COLOR_FormatCbYCrY,
 OMX_COLOR_FormatCrYCbY,
 OMX_COLOR_FormatYUV444Interleaved,
 OMX_COLOR_FormatRawBayer8bit,
 OMX_COLOR_FormatRawBayer10bit,
 OMX_COLOR_FormatRawBayer8bitcompressed,
 OMX_COLOR_FormatL2,
 OMX_COLOR_FormatL4,
 OMX_COLOR_FormatL8,
 OMX_COLOR_FormatL16,
 OMX_COLOR_FormatL24,
 OMX_COLOR_FormatL32,
 OMX_COLOR_FormatYUV420PackedSemiPlanar,
 OMX_COLOR_FormatYUV422PackedSemiPlanar,
 OMX_COLOR_Format18BitBGR666,
 OMX_COLOR_Format24BitARGB6666,
 OMX_COLOR_Format24BitABGR6666) = range(44)

(OMX_COLOR_FormatKhronosExtensions) = 0x6F000000

(OMX_COLOR_FormatVendorStartUnused,  # 0x7F000000
 OMX_COLOR_Format32bitABGR8888,
 OMX_COLOR_Format8bitPalette,
 OMX_COLOR_FormatYUVUV128,
 OMX_COLOR_FormatRawBayer12bit,
 OMX_COLOR_FormatBRCMEGL,
 OMX_COLOR_FormatBRCMOpaque,
 OMX_COLOR_FormatYVU420PackedPlanar,
 OMX_COLOR_FormatYVU420PackedSemiPlanar) = [0x7F000000 + i for i in range(9)]

(OMX_COLOR_FormatMax) = 0x7FFFFFFF

(OMX_DirInput,
 OMX_DirOutput) = range(2)

(OMX_TIME_ClockStateRunning,
 OMX_TIME_ClockStateWaitingForStartTime,
 OMX_TIME_ClockStateStopped) = range(3)

(OMX_TIME_RefClockNone,
 OMX_TIME_RefClockAudio,
 OMX_TIME_RefClockVideo) = range(3)


class COMPONENTTYPE(Structure):
    pass


c_app_data_p = c_char_p
c_handle_p = POINTER(COMPONENTTYPE)


class CORE_BUFFERHEADER_EXTRATYPE(Structure):
    _fields_ = [
            ('nAcquiredPortIndex', c_int),
            ('nAid', c_int)]

class OMX_BUFFERHEADERTYPE(Structure):
    _fields_ = [
        ('nSize', c_int),
        ('nVersion', c_int),
        ('pBuffer', c_void_p),
        ('nAllocLen', c_int),
        ('nFilledLen', c_int),
        ('nOffset', c_int),
        ('pAppPrivate', POINTER(CORE_BUFFERHEADER_EXTRATYPE)),
        ('pPlatformPrivate', c_int),
        ('pInputPortPrivate', c_int),
        ('pOutputPortPrivate', c_int),
        ('hMarkTargetComponent', c_handle_p),
        ('pMarkData', c_int),
        ('nTickCount', c_int),
        ('nTimeStamp', c_int),
        ('nFlags', c_int),
        ('nOutputPortIndex', c_int),
        ('nInputPortIndex', c_int)]

    def get_buffer_p(self):  # Just playing with it.
        return cast(self.pBuffer, POINTER(c_char*self.nAllocLen))
       #return cast(self.pBuffer, POINTER(c_int*self.nAllocLen))


c_buffer_p = c_char_p
c_buffer_header_p = POINTER(OMX_BUFFERHEADERTYPE)
c_int_p = POINTER(c_int)
c_event_handler = CFUNCTYPE(c_int, c_handle_p, c_app_data_p, c_int, c_int, c_int, c_void_p)
c_empty_buffer_done = CFUNCTYPE(c_int, c_handle_p, c_app_data_p, POINTER(OMX_BUFFERHEADERTYPE))
c_fill_buffer_done = CFUNCTYPE(c_int, c_handle_p, c_app_data_p, POINTER(OMX_BUFFERHEADERTYPE))
c_get_component_version = CFUNCTYPE(c_int, c_handle_p, POINTER(c_char*128), c_int_p, c_int_p, POINTER(c_char*128))
c_send_command = CFUNCTYPE(c_int, c_handle_p, c_int, c_int, c_int)
c_get_parameter = CFUNCTYPE(c_int, c_handle_p, c_int, c_void_p)
c_get_config = CFUNCTYPE(c_int, c_handle_p, c_int, c_void_p)
c_set_config = CFUNCTYPE(c_int, c_handle_p, c_int, c_void_p)
c_set_parameter = CFUNCTYPE(c_int, c_handle_p, c_int, c_void_p)
c_get_state = CFUNCTYPE(c_int, c_handle_p, POINTER(c_int))
c_setup_tunnel = CFUNCTYPE(c_int, c_handle_p, c_int, c_handle_p, c_int)
c_allocate_buffer = CFUNCTYPE(c_int, c_handle_p, POINTER(c_buffer_header_p), c_int, c_void_p, c_int)
c_fill_this_buffer = CFUNCTYPE(c_int, c_handle_p, c_buffer_header_p)
c_empty_this_buffer = CFUNCTYPE(c_int, c_handle_p, c_buffer_header_p)
c_free_buffer = CFUNCTYPE(c_int, c_handle_p, c_int, c_buffer_header_p)


class CALLBACKS(Structure):
    _fields_ = [('EventHandler', c_event_handler),
                ('EmptyBufferDone', c_empty_buffer_done),
                ('FillBufferDone', c_fill_buffer_done)]


class OMX_PORT_PARAM_TYPE(Structure):
    _fields_ = [('nSize', c_int),
                ('nVersion', c_int),
                ('nPorts', c_int),
                ('nStartPortNumber', c_int)]


class OMX_IMAGE_PARAM_PORTFORMATTYPE(Structure):
    _fields_ = [('nSize', c_int),
                ('nVersion', c_int),
                ('nPortIndex', c_int),
                ('nIndex', c_int),
                ('eCompressionFormat', c_int),
                ('eColorFormat', c_int)]


class OMX_VIDEO_PARAM_PORTFORMATTYPE(Structure):
    _fields_ = [('nSize', c_int),
                ('nVersion', c_int),
                ('nPortIndex', c_int),
                ('nIndex', c_int),
                ('eCompressionFormat', c_int),
                ('eColorFormat', c_int),
                ('xFramerate', c_int)]


class OMX_AUDIO_PORTDEFINITIONTYPE(Structure):
    _fields_ = [('cMIMEType', c_void_p),  # Not sure about this one.
                ('pNativeRender', c_int),
                ('bFlagErrorConcealment', c_int),
                ('eEncoding', c_int)]

class OMX_VIDEO_PORTDEFINITIONTYPE(Structure):
    _fields_ = [('cMIMEType', c_void_p),  # Nor this one.
                ('pNativeRender', c_void_p),
                ('nFrameWidth', c_uint),
                ('nFrameHeight', c_uint),
                ('nStride', c_int),
                ('nSliceHeight', c_uint),
                ('nBitrate', c_int),
                ('xFramerate', c_int),
                ('bFlagErrorConcealment', c_int),
                ('eCompressionFormat', c_int),     # OMX_VIDEO_CODINGTYPE.
                ('eColorFormat', c_int),           # OMX_COLOR_FORMATTYPE.
                ('pNativeWindow', c_int)]

class OMX_IMAGE_PORTDEFINITIONTYPE(Structure):
    _fields_ = [('cMIMEType', c_void_p),
                ('pNativeRender', c_void_p),
                ('nFrameWidth',  c_uint),
                ('nFrameHeight', c_uint),
                ('nStride', c_int),
                ('nSliceHeight', c_uint),
                ('bFlagErrorConcealment', c_int),
                ('eCompressionFormat', c_int),     # OMX_VIDEO_CODINGTYPE.
                ('eColorFormat', c_int),           # OMX_COLOR_FORMATTYPE.
                ('pNativeWindow', c_int)]

class OMX_OTHER_PORTDEFINITIONTYPE(Structure):
    _fields_ = [('eFormat', c_int)]


class _FORMAT(Union):
    _fields_ = [('audio', OMX_AUDIO_PORTDEFINITIONTYPE),
                ('video', OMX_VIDEO_PORTDEFINITIONTYPE),
                ('image', OMX_IMAGE_PORTDEFINITIONTYPE),
                ('other', OMX_OTHER_PORTDEFINITIONTYPE)]

class OMX_PARAM_PORTDEFINITIONTYPE(Structure):
    _fields_ = [('nSize', c_int),
                ('nVersion', c_int),
                ('nPortIndex', c_int),
                ('eDir', c_int),
                ('nBufferCountActual', c_int),
                ('nBufferCountMin', c_int),
                ('nBufferSize', c_int),
                ('bEnabled', c_int),
                ('bPopulated', c_int),
                ('nBufferCountMin', c_int),
                ('eDomain', c_int),
                ('format', _FORMAT),
               #('format', c_int*12),
                ('bBuffersContiguous', c_int),
                ('nBufferAlignment', c_int)]


_not_implemented = CFUNCTYPE(c_int)

COMPONENTTYPE._fields_ = [('nSize', c_int),
                          ('nVersion', c_int),
                          ('pComponentPrivate', c_int),
                          ('pApplicationPrivate', c_int),
                          ('GetComponentVersion',c_get_component_version),
                          ('SendCommand', c_send_command),
                          ('GetParameter', c_get_parameter),
                          ('SetParameter', c_set_parameter),
                          ('GetConfig', c_get_config),
                          ('SetConfig', c_set_config),
                          ('GetExtensionIndex', _not_implemented),
                          ('GetState', c_get_state),
                          ('ComponentTunnelRequest', _not_implemented),
                          ('UseBuffer', _not_implemented),
                          ('AllocateBuffer', c_allocate_buffer),
                          ('FreeBuffer', c_free_buffer),
                          ('EmptyThisBuffer', c_empty_this_buffer),
                          ('FillThisBuffer', c_fill_this_buffer),
                          ('ComponentTunnelRequest', _not_implemented),
                          ('SetCallbacks', _not_implemented),
                          ('ComponentDeInit', _not_implemented),
                          ('UseEGLImage', _not_implemented),
                          ('ComponentRoleEnum', _not_implemented)]


class OMX_PARAM_CONTENTURITYPE(Structure):
    _fields_ = [('nSize', c_int),
                ('nVersion', c_int),
                ('contentURI', c_char*256)]


class OMX_PARAM_U32TYPE(Structure):
     _fields_ = [('nSize', c_int),
                 ('nVersion', c_int),
                 ('nPortIndex', c_int),
                 ('nU32', c_int)]


class OMX_TIME_CONFIG_CLOCKSTATETYPE(Structure):
     _fields_ = [('nSize', c_int),
                 ('nVersion', c_int),
                 ('eState', c_int),
                 ('nStartTime0', c_int),
                 ('nStartTime1', c_int),
                 ('nOffset0', c_int),
                 ('nOffset1', c_int),
                 ('nWaitMask', c_int)]


class OMX_TIME_CONFIG_TIMESTAMPTYPE(Structure):
     _fields_ = [('nSize', c_int),
                 ('nVersion', c_int),
                 ('nPortIndex', c_int),
                 ('nTimestamp0', c_int),
                 ('nTimestamp1', c_int)]


class OMX_TIME_CONFIG_SCALETYPE(Structure):
     _fields_ = [('nSize', c_int),
                 ('nVersion', c_int),
                 ('xScale', c_int)] # Q16


class OMX_TIME_CONFIG_ACTIVEREFCLOCKTYPE(Structure):
     _fields_ = [('nSize', c_int),
                 ('nVersion', c_int),
                 ('eClock', c_int)]



bcm = CDLL('libbcm_host.so')
assert bcm.bcm_host_init() == 0

openmax = CDLL('libopenmaxil.so')
assert openmax.OMX_Init() == 0

