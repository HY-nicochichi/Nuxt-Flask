export type Input = {
  label: string
  type: string
  value: string
  validation: (val: string) => boolean
}
