import torch
import os
from adgdit.config import get_args
from adgdit.modules.models import ADG_DIT_MODELS

from adgdit.inference import _to_tuple

model_path = "/mnt/ssd/ADG-DiT/ADG-DiT_XL_2_ADoldversion/003-dit_XL_2/checkpoints/e4800.pt/zero_pp_rank_0_mp_rank_00_optim_states.pt"  # Replace with your model path
args = get_args()

image_size = _to_tuple(args.image_size)
latent_size = (image_size[0] // 8, image_size[1] // 8)

model = ADG_DIT_MODELS[args.model](args,
                                       input_size=latent_size,
                                       log_fn=print,
                                        )

# model_path = os.path.join(args.model_root, 't2i', 'model', f"pytorch_model_{args.load_key}.pt")
state_dict = torch.load(model_path, map_location=lambda storage, loc: storage)

print(f"Loading model from {model_path}")
model.load_state_dict(state_dict)

print(f"Loading lora from {args.lora_ckpt}")
model.load_adapter(args.lora_ckpt)
model.merge_and_unload()

torch.save(model.state_dict(), args.output_merge_path)
print(f"Model saved to {args.output_merge_path}")