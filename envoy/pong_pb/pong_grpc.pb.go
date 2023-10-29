// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v3.6.1
// source: pong_pb/pong.proto

package pong_pb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

const (
	EchoService_PongHello_FullMethodName = "/pong_pb.EchoService/PongHello"
	EchoService_PongWorld_FullMethodName = "/pong_pb.EchoService/PongWorld"
)

// EchoServiceClient is the client API for EchoService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type EchoServiceClient interface {
	PongHello(ctx context.Context, in *PongHelloRequest, opts ...grpc.CallOption) (*PongHelloResponse, error)
	PongWorld(ctx context.Context, in *PongWorldRequest, opts ...grpc.CallOption) (*PongWorldResponse, error)
}

type echoServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewEchoServiceClient(cc grpc.ClientConnInterface) EchoServiceClient {
	return &echoServiceClient{cc}
}

func (c *echoServiceClient) PongHello(ctx context.Context, in *PongHelloRequest, opts ...grpc.CallOption) (*PongHelloResponse, error) {
	out := new(PongHelloResponse)
	err := c.cc.Invoke(ctx, EchoService_PongHello_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *echoServiceClient) PongWorld(ctx context.Context, in *PongWorldRequest, opts ...grpc.CallOption) (*PongWorldResponse, error) {
	out := new(PongWorldResponse)
	err := c.cc.Invoke(ctx, EchoService_PongWorld_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// EchoServiceServer is the server API for EchoService service.
// All implementations must embed UnimplementedEchoServiceServer
// for forward compatibility
type EchoServiceServer interface {
	PongHello(context.Context, *PongHelloRequest) (*PongHelloResponse, error)
	PongWorld(context.Context, *PongWorldRequest) (*PongWorldResponse, error)
	mustEmbedUnimplementedEchoServiceServer()
}

// UnimplementedEchoServiceServer must be embedded to have forward compatible implementations.
type UnimplementedEchoServiceServer struct {
}

func (UnimplementedEchoServiceServer) PongHello(context.Context, *PongHelloRequest) (*PongHelloResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PongHello not implemented")
}
func (UnimplementedEchoServiceServer) PongWorld(context.Context, *PongWorldRequest) (*PongWorldResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PongWorld not implemented")
}
func (UnimplementedEchoServiceServer) mustEmbedUnimplementedEchoServiceServer() {}

// UnsafeEchoServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to EchoServiceServer will
// result in compilation errors.
type UnsafeEchoServiceServer interface {
	mustEmbedUnimplementedEchoServiceServer()
}

func RegisterEchoServiceServer(s grpc.ServiceRegistrar, srv EchoServiceServer) {
	s.RegisterService(&EchoService_ServiceDesc, srv)
}

func _EchoService_PongHello_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PongHelloRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(EchoServiceServer).PongHello(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: EchoService_PongHello_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(EchoServiceServer).PongHello(ctx, req.(*PongHelloRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _EchoService_PongWorld_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PongWorldRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(EchoServiceServer).PongWorld(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: EchoService_PongWorld_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(EchoServiceServer).PongWorld(ctx, req.(*PongWorldRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// EchoService_ServiceDesc is the grpc.ServiceDesc for EchoService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var EchoService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "pong_pb.EchoService",
	HandlerType: (*EchoServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "PongHello",
			Handler:    _EchoService_PongHello_Handler,
		},
		{
			MethodName: "PongWorld",
			Handler:    _EchoService_PongWorld_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "pong_pb/pong.proto",
}