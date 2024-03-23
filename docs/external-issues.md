# Issues found while doing this

## pyscsi

PySCSI currently cannot be used to write to SCSI devices on Linux. PR submitted

## Linux Kernel

Unplugging the device while accessing it reliably leads to a null pointer
dereference in the Linux kernel. This needs further investigation.

```
Mär 23 10:32:42 laptop-jge kernel: BUG: kernel NULL pointer dereference, address: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: #PF: supervisor write access in kernel mode
Mär 23 10:32:42 laptop-jge kernel: #PF: error_code(0x0002) - not-present page
Mär 23 10:32:42 laptop-jge kernel: PGD 0 P4D 0 
Mär 23 10:32:42 laptop-jge kernel: Oops: 0002 [#1] PREEMPT SMP PTI
Mär 23 10:32:42 laptop-jge kernel: CPU: 0 PID: 95775 Comm: kworker/0:0 Tainted: G          IOE      6.7.9-200.fc39.x86_64 #1
Mär 23 10:32:42 laptop-jge kernel: Hardware name: LENOVO 20CMCTO1WW/20CMCTO1WW, BIOS N10ET61W (1.40 ) 03/17/2020
Mär 23 10:32:42 laptop-jge kernel: Workqueue: events sg_remove_sfp_usercontext
Mär 23 10:32:42 laptop-jge kernel: RIP: 0010:mutex_lock+0x1d/0x30
Mär 23 10:32:42 laptop-jge kernel: Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 0f 1f 44 00 00 53 48 89 fb e8 0e db ff ff 31 c0 65 48 8b 14 25 40 39 03 00 <f0> 48 0f b1 13 75 06 5b c3 cc cc cc cc 48 89 df 5b eb b0 90 90 90
Mär 23 10:32:42 laptop-jge kernel: RSP: 0000:ffffa321815ebdd0 EFLAGS: 00010246
Mär 23 10:32:42 laptop-jge kernel: RAX: 0000000000000000 RBX: 0000000000000398 RCX: 00000000020001f5
Mär 23 10:32:42 laptop-jge kernel: RDX: ffff918368dc28c0 RSI: ffffdd0184001c80 RDI: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: RBP: 0000000000000000 R08: 0000000000000000 R09: 00000000020001f5
Mär 23 10:32:42 laptop-jge kernel: R10: ffff918300072d90 R11: 0000000000000110 R12: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: R13: ffff9185a4ada000 R14: ffff91830015bc05 R15: ffff9183592b5328
Mär 23 10:32:42 laptop-jge kernel: FS:  0000000000000000(0000) GS:ffff91863dc00000(0000) knlGS:0000000000000000
Mär 23 10:32:42 laptop-jge kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Mär 23 10:32:42 laptop-jge kernel: CR2: 0000000000000398 CR3: 0000000186b2e005 CR4: 00000000003706f0
Mär 23 10:32:42 laptop-jge kernel: Call Trace:
Mär 23 10:32:42 laptop-jge kernel:  <TASK>
Mär 23 10:32:42 laptop-jge kernel:  ? __die+0x23/0x70
Mär 23 10:32:42 laptop-jge kernel:  ? page_fault_oops+0x171/0x4e0
Mär 23 10:32:42 laptop-jge kernel:  ? __slab_free+0xf1/0x330
Mär 23 10:32:42 laptop-jge kernel:  ? exc_page_fault+0x7f/0x180
Mär 23 10:32:42 laptop-jge kernel:  ? asm_exc_page_fault+0x26/0x30
Mär 23 10:32:42 laptop-jge kernel:  ? mutex_lock+0x1d/0x30
Mär 23 10:32:42 laptop-jge kernel:  blk_trace_remove+0x1a/0x70
Mär 23 10:32:42 laptop-jge kernel:  sg_device_destroy+0x26/0xa0
Mär 23 10:32:42 laptop-jge kernel:  sg_remove_sfp_usercontext+0x141/0x1a0
Mär 23 10:32:42 laptop-jge kernel:  process_one_work+0x174/0x340
Mär 23 10:32:42 laptop-jge kernel:  worker_thread+0x27b/0x3a0
Mär 23 10:32:42 laptop-jge kernel:  ? __pfx_worker_thread+0x10/0x10
Mär 23 10:32:42 laptop-jge kernel:  kthread+0xe8/0x120
Mär 23 10:32:42 laptop-jge kernel:  ? __pfx_kthread+0x10/0x10
Mär 23 10:32:42 laptop-jge kernel:  ret_from_fork+0x34/0x50
Mär 23 10:32:42 laptop-jge kernel:  ? __pfx_kthread+0x10/0x10
Mär 23 10:32:42 laptop-jge kernel:  ret_from_fork_asm+0x1b/0x30
Mär 23 10:32:42 laptop-jge kernel:  </TASK>
Mär 23 10:32:42 laptop-jge kernel: Modules linked in: hid_apple hidp uhid uas usb_storage uinput rfcomm snd_seq_dummy snd_hrtimer xt_CHECKSUM xt_MASQUERADE xt_conntrack ipt_REJECT nf_reject_ipv4 ip6table_mangle ip6table_nat ip6table_filter iptable_mangle iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter bridge stp llc vboxnetadp(OE) vboxnetflt(OE) vboxdrv(OE) qrtr bnep iwlmvm intel_rapl_msr rmi_smbus intel_rapl_common x86_pkg_temp_thermal rmi_cor>
Mär 23 10:32:42 laptop-jge kernel:  lpc_ich intel_pch_thermal mei rfkill i2c_smbus snd soundcore joydev loop zram mmc_block i915 rtsx_pci_sdmmc i2c_algo_bit drm_buddy crct10dif_pclmul mmc_core crc32_pclmul ttm crc32c_intel polyval_clmulni polyval_generic e1000e ghash_clmulni_intel sha512_ssse3 drm_display_helper sha256_ssse3 sha1_ssse3 rtsx_pci cec video wmi serio_raw scsi_dh_rdac scsi_dh_emc scsi_dh_alua ip6_tables ip_tables dm_multipath fuse
Mär 23 10:32:42 laptop-jge kernel: CR2: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: ---[ end trace 0000000000000000 ]---
Mär 23 10:32:42 laptop-jge kernel: RIP: 0010:mutex_lock+0x1d/0x30
Mär 23 10:32:42 laptop-jge kernel: Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 0f 1f 44 00 00 53 48 89 fb e8 0e db ff ff 31 c0 65 48 8b 14 25 40 39 03 00 <f0> 48 0f b1 13 75 06 5b c3 cc cc cc cc 48 89 df 5b eb b0 90 90 90
Mär 23 10:32:42 laptop-jge kernel: RSP: 0000:ffffa321815ebdd0 EFLAGS: 00010246
Mär 23 10:32:42 laptop-jge kernel: RAX: 0000000000000000 RBX: 0000000000000398 RCX: 00000000020001f5
Mär 23 10:32:42 laptop-jge kernel: RDX: ffff918368dc28c0 RSI: ffffdd0184001c80 RDI: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: RBP: 0000000000000000 R08: 0000000000000000 R09: 00000000020001f5
Mär 23 10:32:42 laptop-jge kernel: R10: ffff918300072d90 R11: 0000000000000110 R12: 0000000000000398
Mär 23 10:32:42 laptop-jge kernel: R13: ffff9185a4ada000 R14: ffff91830015bc05 R15: ffff9183592b5328
Mär 23 10:32:42 laptop-jge kernel: FS:  0000000000000000(0000) GS:ffff91863dc00000(0000) knlGS:0000000000000000
Mär 23 10:32:42 laptop-jge kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Mär 23 10:32:42 laptop-jge kernel: CR2: 0000000000000398 CR3: 0000000186b2e005 CR4: 000
```
