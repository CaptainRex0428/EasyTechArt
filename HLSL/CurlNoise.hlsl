// - UVs (Vector2)
// - NoiseTexture (Texture Object)
// - Scale (float2, default: 1.0,1.0)
// - Offset (float2, default: 1.0,1.0)
// - SampleOffset (Scalar, default: 0.01)

float2 uv = (UVs + Offset) * Scale;
float offset = SampleOffset;

float3 n_center = Texture2DSample(NoiseTexture, NoiseTextureSampler, uv);
float3 n_right = Texture2DSample(NoiseTexture, NoiseTextureSampler, uv + float2(offset, 0));
float3 n_left = Texture2DSample(NoiseTexture, NoiseTextureSampler, uv - float2(offset, 0));
float3 n_up = Texture2DSample(NoiseTexture, NoiseTextureSampler, uv + float2(0, offset));
float3 n_down = Texture2DSample(NoiseTexture, NoiseTextureSampler, uv - float2(0, offset));

// 偏导数
float3 dF_dx = (n_right - n_left) / (2.0 * offset);
float3 dF_dy = (n_up - n_down) / (2.0 * offset);

// 2D Curl (R)
float2 curl2D = float2(dF_dy.r, -dF_dx.r);

// 或3D Curl
float3 curl3D = float3(
    dF_dy.g,
    -dF_dx.b,
    dF_dy.r - dF_dx.g
);

return curl2D; // 或 curl3D