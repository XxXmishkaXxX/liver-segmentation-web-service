import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export const toastMixin = {
  methods: {
    showInfoMessage(info) {
      toast.info(info, {
        autoClose: 3000,
      });
    },
    showSuccessMessage(successMessage) {
      toast.success(successMessage, {
        autoClose: 3000,
      });
    },
    showErrorMessage(error) {
      toast.error(error, {
        autoClose: 3000,
      });
    }
  }
};