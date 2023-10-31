// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v3.6.1
// source: ping_pb/ping.proto

package ping_pb

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
	PingService_PingHello_FullMethodName = "/ping_pb.PingService/PingHello"
	PingService_PingWorld_FullMethodName = "/ping_pb.PingService/PingWorld"
)

// PingServiceClient is the client API for PingService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type PingServiceClient interface {
	PingHello(ctx context.Context, in *PingHelloRequest, opts ...grpc.CallOption) (*PingHelloResponse, error)
	PingWorld(ctx context.Context, in *PingWorldRequest, opts ...grpc.CallOption) (*PingWorldResponse, error)
}

type pingServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewPingServiceClient(cc grpc.ClientConnInterface) PingServiceClient {
	return &pingServiceClient{cc}
}

func (c *pingServiceClient) PingHello(ctx context.Context, in *PingHelloRequest, opts ...grpc.CallOption) (*PingHelloResponse, error) {
	out := new(PingHelloResponse)
	err := c.cc.Invoke(ctx, PingService_PingHello_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *pingServiceClient) PingWorld(ctx context.Context, in *PingWorldRequest, opts ...grpc.CallOption) (*PingWorldResponse, error) {
	out := new(PingWorldResponse)
	err := c.cc.Invoke(ctx, PingService_PingWorld_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// PingServiceServer is the server API for PingService service.
// All implementations must embed UnimplementedPingServiceServer
// for forward compatibility
type PingServiceServer interface {
	PingHello(context.Context, *PingHelloRequest) (*PingHelloResponse, error)
	PingWorld(context.Context, *PingWorldRequest) (*PingWorldResponse, error)
	mustEmbedUnimplementedPingServiceServer()
}

// UnimplementedPingServiceServer must be embedded to have forward compatible implementations.
type UnimplementedPingServiceServer struct {
}

func (UnimplementedPingServiceServer) PingHello(context.Context, *PingHelloRequest) (*PingHelloResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PingHello not implemented")
}
func (UnimplementedPingServiceServer) PingWorld(context.Context, *PingWorldRequest) (*PingWorldResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method PingWorld not implemented")
}
func (UnimplementedPingServiceServer) mustEmbedUnimplementedPingServiceServer() {}

// UnsafePingServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to PingServiceServer will
// result in compilation errors.
type UnsafePingServiceServer interface {
	mustEmbedUnimplementedPingServiceServer()
}

func RegisterPingServiceServer(s grpc.ServiceRegistrar, srv PingServiceServer) {
	s.RegisterService(&PingService_ServiceDesc, srv)
}

func _PingService_PingHello_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PingHelloRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PingServiceServer).PingHello(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: PingService_PingHello_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PingServiceServer).PingHello(ctx, req.(*PingHelloRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _PingService_PingWorld_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PingWorldRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PingServiceServer).PingWorld(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: PingService_PingWorld_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PingServiceServer).PingWorld(ctx, req.(*PingWorldRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// PingService_ServiceDesc is the grpc.ServiceDesc for PingService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var PingService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "ping_pb.PingService",
	HandlerType: (*PingServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "PingHello",
			Handler:    _PingService_PingHello_Handler,
		},
		{
			MethodName: "PingWorld",
			Handler:    _PingService_PingWorld_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "ping_pb/ping.proto",
}
