// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0
// 	protoc        v3.6.1
// source: ping_pb/ping.proto

package ping_pb

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type PingHelloRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Body string `protobuf:"bytes,1,opt,name=body,proto3" json:"body,omitempty"`
}

func (x *PingHelloRequest) Reset() {
	*x = PingHelloRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_ping_pb_ping_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *PingHelloRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PingHelloRequest) ProtoMessage() {}

func (x *PingHelloRequest) ProtoReflect() protoreflect.Message {
	mi := &file_ping_pb_ping_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PingHelloRequest.ProtoReflect.Descriptor instead.
func (*PingHelloRequest) Descriptor() ([]byte, []int) {
	return file_ping_pb_ping_proto_rawDescGZIP(), []int{0}
}

func (x *PingHelloRequest) GetBody() string {
	if x != nil {
		return x.Body
	}
	return ""
}

type PingHelloResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Body string `protobuf:"bytes,1,opt,name=body,proto3" json:"body,omitempty"`
}

func (x *PingHelloResponse) Reset() {
	*x = PingHelloResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_ping_pb_ping_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *PingHelloResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PingHelloResponse) ProtoMessage() {}

func (x *PingHelloResponse) ProtoReflect() protoreflect.Message {
	mi := &file_ping_pb_ping_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PingHelloResponse.ProtoReflect.Descriptor instead.
func (*PingHelloResponse) Descriptor() ([]byte, []int) {
	return file_ping_pb_ping_proto_rawDescGZIP(), []int{1}
}

func (x *PingHelloResponse) GetBody() string {
	if x != nil {
		return x.Body
	}
	return ""
}

type PingWorldRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Body string `protobuf:"bytes,1,opt,name=body,proto3" json:"body,omitempty"`
}

func (x *PingWorldRequest) Reset() {
	*x = PingWorldRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_ping_pb_ping_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *PingWorldRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PingWorldRequest) ProtoMessage() {}

func (x *PingWorldRequest) ProtoReflect() protoreflect.Message {
	mi := &file_ping_pb_ping_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PingWorldRequest.ProtoReflect.Descriptor instead.
func (*PingWorldRequest) Descriptor() ([]byte, []int) {
	return file_ping_pb_ping_proto_rawDescGZIP(), []int{2}
}

func (x *PingWorldRequest) GetBody() string {
	if x != nil {
		return x.Body
	}
	return ""
}

type PingWorldResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Body string `protobuf:"bytes,1,opt,name=body,proto3" json:"body,omitempty"`
}

func (x *PingWorldResponse) Reset() {
	*x = PingWorldResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_ping_pb_ping_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *PingWorldResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PingWorldResponse) ProtoMessage() {}

func (x *PingWorldResponse) ProtoReflect() protoreflect.Message {
	mi := &file_ping_pb_ping_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PingWorldResponse.ProtoReflect.Descriptor instead.
func (*PingWorldResponse) Descriptor() ([]byte, []int) {
	return file_ping_pb_ping_proto_rawDescGZIP(), []int{3}
}

func (x *PingWorldResponse) GetBody() string {
	if x != nil {
		return x.Body
	}
	return ""
}

var File_ping_pb_ping_proto protoreflect.FileDescriptor

var file_ping_pb_ping_proto_rawDesc = []byte{
	0x0a, 0x12, 0x70, 0x69, 0x6e, 0x67, 0x5f, 0x70, 0x62, 0x2f, 0x70, 0x69, 0x6e, 0x67, 0x2e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x12, 0x07, 0x70, 0x69, 0x6e, 0x67, 0x5f, 0x70, 0x62, 0x22, 0x26, 0x0a,
	0x10, 0x50, 0x69, 0x6e, 0x67, 0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x12, 0x12, 0x0a, 0x04, 0x62, 0x6f, 0x64, 0x79, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x04, 0x62, 0x6f, 0x64, 0x79, 0x22, 0x27, 0x0a, 0x11, 0x50, 0x69, 0x6e, 0x67, 0x48, 0x65, 0x6c,
	0x6c, 0x6f, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x62, 0x6f,
	0x64, 0x79, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x62, 0x6f, 0x64, 0x79, 0x22, 0x26,
	0x0a, 0x10, 0x50, 0x69, 0x6e, 0x67, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x52, 0x65, 0x71, 0x75, 0x65,
	0x73, 0x74, 0x12, 0x12, 0x0a, 0x04, 0x62, 0x6f, 0x64, 0x79, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09,
	0x52, 0x04, 0x62, 0x6f, 0x64, 0x79, 0x22, 0x27, 0x0a, 0x11, 0x50, 0x69, 0x6e, 0x67, 0x57, 0x6f,
	0x72, 0x6c, 0x64, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x62,
	0x6f, 0x64, 0x79, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x62, 0x6f, 0x64, 0x79, 0x32,
	0x95, 0x01, 0x0a, 0x0b, 0x50, 0x69, 0x6e, 0x67, 0x53, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x12,
	0x42, 0x0a, 0x09, 0x50, 0x69, 0x6e, 0x67, 0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x12, 0x19, 0x2e, 0x70,
	0x69, 0x6e, 0x67, 0x5f, 0x70, 0x62, 0x2e, 0x50, 0x69, 0x6e, 0x67, 0x48, 0x65, 0x6c, 0x6c, 0x6f,
	0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x1a, 0x2e, 0x70, 0x69, 0x6e, 0x67, 0x5f, 0x70,
	0x62, 0x2e, 0x50, 0x69, 0x6e, 0x67, 0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x52, 0x65, 0x73, 0x70, 0x6f,
	0x6e, 0x73, 0x65, 0x12, 0x42, 0x0a, 0x09, 0x50, 0x69, 0x6e, 0x67, 0x57, 0x6f, 0x72, 0x6c, 0x64,
	0x12, 0x19, 0x2e, 0x70, 0x69, 0x6e, 0x67, 0x5f, 0x70, 0x62, 0x2e, 0x50, 0x69, 0x6e, 0x67, 0x57,
	0x6f, 0x72, 0x6c, 0x64, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x1a, 0x2e, 0x70, 0x69,
	0x6e, 0x67, 0x5f, 0x70, 0x62, 0x2e, 0x50, 0x69, 0x6e, 0x67, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x52,
	0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x42, 0x0b, 0x5a, 0x09, 0x2e, 0x2f, 0x70, 0x69, 0x6e,
	0x67, 0x5f, 0x70, 0x62, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_ping_pb_ping_proto_rawDescOnce sync.Once
	file_ping_pb_ping_proto_rawDescData = file_ping_pb_ping_proto_rawDesc
)

func file_ping_pb_ping_proto_rawDescGZIP() []byte {
	file_ping_pb_ping_proto_rawDescOnce.Do(func() {
		file_ping_pb_ping_proto_rawDescData = protoimpl.X.CompressGZIP(file_ping_pb_ping_proto_rawDescData)
	})
	return file_ping_pb_ping_proto_rawDescData
}

var file_ping_pb_ping_proto_msgTypes = make([]protoimpl.MessageInfo, 4)
var file_ping_pb_ping_proto_goTypes = []interface{}{
	(*PingHelloRequest)(nil),  // 0: ping_pb.PingHelloRequest
	(*PingHelloResponse)(nil), // 1: ping_pb.PingHelloResponse
	(*PingWorldRequest)(nil),  // 2: ping_pb.PingWorldRequest
	(*PingWorldResponse)(nil), // 3: ping_pb.PingWorldResponse
}
var file_ping_pb_ping_proto_depIdxs = []int32{
	0, // 0: ping_pb.PingService.PingHello:input_type -> ping_pb.PingHelloRequest
	2, // 1: ping_pb.PingService.PingWorld:input_type -> ping_pb.PingWorldRequest
	1, // 2: ping_pb.PingService.PingHello:output_type -> ping_pb.PingHelloResponse
	3, // 3: ping_pb.PingService.PingWorld:output_type -> ping_pb.PingWorldResponse
	2, // [2:4] is the sub-list for method output_type
	0, // [0:2] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_ping_pb_ping_proto_init() }
func file_ping_pb_ping_proto_init() {
	if File_ping_pb_ping_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_ping_pb_ping_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*PingHelloRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_ping_pb_ping_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*PingHelloResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_ping_pb_ping_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*PingWorldRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_ping_pb_ping_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*PingWorldResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_ping_pb_ping_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   4,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_ping_pb_ping_proto_goTypes,
		DependencyIndexes: file_ping_pb_ping_proto_depIdxs,
		MessageInfos:      file_ping_pb_ping_proto_msgTypes,
	}.Build()
	File_ping_pb_ping_proto = out.File
	file_ping_pb_ping_proto_rawDesc = nil
	file_ping_pb_ping_proto_goTypes = nil
	file_ping_pb_ping_proto_depIdxs = nil
}
