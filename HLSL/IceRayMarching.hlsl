// ViewDirection
// NormalVector
// Position
// CameraWP
// ObjectToWorldPosition

// RefractionSurfaceNoise
// Refraction

// StepLength
// StepCount

// LinearMaskVector
// LinearMaskOffset
// LinearMaskScale
// LinearMaskNegate

// NoiseStrength
// NoiseExp
// NoiseIntersection

// WeightScale

float VolumeNoiseScale  =   NoiseScale * 0.001;

float2 OutputPom;

float StepDistance = .0f;
OutputPom.r = .0f;
OutputPom.g = .0f;

ViewDirection = normalize(ViewDirection);
NormalVector = normalize(NormalVector);

float3 RefractVector = refract(ViewDirection,NormalVector,saturate(1-(RefractionSurfaceNoise/Refraction)));

float3 SampledPosition;
float3 SampledCustomNoise;
float3 LinearMask;

float WeightR = 0.0f;
float WeightG = 0.0f;

for (int MarchingIdx = 0; MarchingIdx < StepCount; ++MarchingIdx)
{
    SampledPosition = Position + RefractVector * StepDistance;
    SampledPosition *= VolumeNoiseScale;

    float3 sampledCustomNoiseXY = Texture2DSample(VolumeNoise, VolumeNoiseSampler, SampledPosition.xy );
    float3 sampledCustomNoiseZY = Texture2DSample(VolumeNoise, VolumeNoiseSampler, SampledPosition.zy + float2(144.23, 5444.12));
    float3 sampledCustomNoiseXZ = Texture2DSample(VolumeNoise, VolumeNoiseSampler, SampledPosition.xz + float2(3127.11, 1522.12));

    SampledCustomNoise = sampledCustomNoiseXY * sampledCustomNoiseZY * sampledCustomNoiseXZ;

    LinearMask = saturate((saturate(dot(SampledPosition, LinearMaskVector) + LinearMaskOffset) * LinearMaskScale) + LinearMaskNegate);

    float WeightX = saturate(1.0-(MarchingIdx/StepCount));
    OutputPom.r += saturate((SampledCustomNoise.x * NoiseStrength))  * LinearMask * WeightX;

    float WeightY = saturate((MarchingIdx + 1)/StepCount);
    OutputPom.g += pow(SampledCustomNoise.y, NoiseExp) * LinearMask * 2 * saturate((MarchingIdx + 1)/StepCount);

    WeightR += WeightX;
    WeightG += WeightY;

    StepDistance += (StepLength / StepCount);
}

OutputPom.r /= WeightR;
OutputPom.g /= WeightG;

OutputPom *= WeightScale;

DebugCloud = OutputPom.r;
DebugVoronoi = OutputPom.g;
DebugRefractVector = RefractVector;
DebugLinearMask = LinearMask;

return OutputPom.r  + (saturate(OutputPom.r + (1 - NoiseIntersection)) * OutputPom.g );
