#include <memory>
#include <iostream>

#include "MvCameraControl.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include "pch.h"
#include "pybind11/pybind11.h"
#undef max
#include "pybind11/numpy.h"

namespace py = pybind11;

class HKDriver
{
private:
	void* _handle;
	unsigned int _g_npayloadsize;
	unsigned char* _pbuffer;
	MV_FRAME_OUT_INFO_EX _stimginfo;
	int _w, _h;

public:
	HKDriver(): 
		//_nret(MV_OK),
		_handle(nullptr),
		_g_npayloadsize(static_cast<unsigned int>(0)),
		_stimginfo({ 0 })
	{
		int nret = MV_OK;
		MV_CC_DEVICE_INFO_LIST stdevlist;

		std::memset(&stdevlist, 0, sizeof(stdevlist));
		nret = MV_CC_EnumDevices(MV_USB_DEVICE, &stdevlist);
		if (nret != MV_OK)
		{
			// 抛个异常把 别print了
			std::cout << "enum dev fail" << std::endl;
		}

		// 严格限定只能有一个设备
		if (stdevlist.nDeviceNum != 1)
		{
			std::cout << "dev number error" << std::endl;
		}

		nret = MV_CC_CreateHandle(&_handle, stdevlist.pDeviceInfo[0]);
		if (nret != MV_OK)
		{
			// throw error
			std::cout << "create handle failed" << std::endl;
		}

		nret = MV_CC_OpenDevice(_handle);
		if (nret != MV_OK)
		{
			// throw error
			std::cout << "open dev fail" << std::endl;
		}

		nret = MV_CC_SetEnumValue(_handle, "TriggerMode", 0);
		if (nret != MV_OK)
		{
			// throw error
			std::cout << "set trigger mode failed" << std::endl;
		}

		MVCC_INTVALUE st_param;
		memset(&st_param, 0, sizeof(MVCC_INTVALUE));
		nret = MV_CC_GetIntValue(_handle, "PayloadSize", &st_param);
		if (nret != MV_OK)
		{
			// throw
			std::cout << "get payload size failed." << std::endl;
		}

		_g_npayloadsize = st_param.nCurValue;
		_pbuffer = new unsigned char[_g_npayloadsize];
		memset(&_stimginfo, 0, sizeof(MV_FRAME_OUT_INFO_EX));
	}

	bool init()
	{
		auto nret = MV_CC_StartGrabbing(_handle);
		return nret == MV_OK ? true : false;
	}

	unsigned char * load_img_buffer()
	{
		auto nret = MV_CC_GetOneFrameTimeout(_handle, _pbuffer, _g_npayloadsize, &_stimginfo, 1000);
		if (nret != MV_OK)
		{
			std::cout << "grab img fail" << std::endl;
		}
		_w = _stimginfo.nWidth;
		_h = _stimginfo.nHeight;

		return _pbuffer;
	}

	const int getwidth() const { return _w; }

	const int getheight() const { return _h; }

	const int size() const { return _g_npayloadsize; }
};


PYBIND11_MODULE(hkdriver, m)
{
	py::class_<HKDriver>(m, "HKDriver", py::buffer_protocol())
		.def(py::init())
		.def_buffer(
			[](HKDriver& d) -> py::buffer_info
			{
				return py::buffer_info(
					d.load_img_buffer(),
					sizeof(unsigned char),
					py::format_descriptor<unsigned char>::format(),
					1,
					{ d.size() },
					{sizeof(unsigned char)}
				);
			}
		)
		.def_property_readonly("width", &HKDriver::getwidth)
				.def_property_readonly("height", &HKDriver::getheight)
				.def("init", &HKDriver::init);
}