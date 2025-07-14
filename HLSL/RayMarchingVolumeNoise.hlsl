// ViewDirection
// Position
// CameraWP
// NormalVector
// ObjectToWorldPosition

// RefractionSurfaceNoise
// Refraction

// stepLength

// VolumeNoise
// VolumeNoiseSamplerr
// VolumeNoiseScale
// NoiseStrength
// NoisePow

// VolumeNoise2
// VolumeNoise2Exp
// VolumeNoise2Scale
// VolumeNoise2Multiply

// LinearMaskScale
// LinearMaskNegate
// LinearMaskOffset
// LinearMaskVector
// LinearMaskVectorWorldOffset

float2 outputpom;

float step = 0.0;
float final = 0.0;
float final2 = 0.0;

float3 sampledPosition;

for (int i = 0; i < 8; i++)
{
    sampledPosition = Position + refract(normalize(ViewDirection), NormalVector, saturate(1-(RefractionSurfaceNoise / Refraction))) * step;
    
    float2 sampledCustomNoise = Texture2DSample(VolumeNoise, VolumeNoiseSampler, sampledPosition.xy * VolumeNoiseScale) * Texture2DSample(VolumeNoise, VolumeNoiseSampler, sampledPosition.zy * VolumeNoiseScale + float2(144.23, 5444.12));
    sampledCustomNoise *= Texture2DSample(VolumeNoise, VolumeNoiseSampler, sampledPosition.xz * VolumeNoiseScale + float2(3127.11, 1522.12));

    float linearMask = saturate(saturate((dot(sampledPosition - LinearMaskVectorWorldOffset, LinearMaskVector) + LinearMaskOffset) * LinearMaskScale) + LinearMaskNegate);

    final += pow(saturate((pow(sampledCustomNoise.x, NoisePow) * NoiseStrength * 1.45)), 1.25) * saturate(1.0-(i/20.0)) * linearMask;
    final2 += pow(sampledCustomNoise.y, VolumeNoise2Exp * 0.95) * VolumeNoise2Multiply * 2.00 * linearMask;

    step += (stepLength/8.0);
}

outputpom.x = final;
outputpom.y = final2;
return outputpom;